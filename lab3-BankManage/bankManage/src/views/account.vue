<template>
    <div v-loading="loading">
        <h1>账户管理</h1>
        <p style="color: red;font-size: 24px;" align="left">条件筛选</p>
        <div align="left">
            账户号
            <input
                type="text"
                placeholder="包含关键字"
                id="idSearch"
                v-model="idSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;户主
            <input
                type="text"
                placeholder="包含关键字"
                id="ownerSearch"
                v-model="ownerSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;开户银行
            <input
                type="text"
                placeholder="包含关键字"
                id="bankSearch"
                v-model="bankSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;账户类型
            <select v-model="typeSearch" id="typeSearch" placeholder="any">
                <option value="any" selected>任意</option>
                <option value="saving">储蓄账户</option>
                <option value="check">支票账户</option> </select
            ><br /><br />余额
            <input
                type="number"
                min="0"
                placeholder="下界"
                id="money_lo"
                v-model="money_lo"
                required="false"
                style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />~~
            <input
                type="number"
                min="0"
                placeholder="上界"
                id="money_up"
                v-model="money_up"
                required="false"
                style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;开户日期
            <input
                type="date"
                min="0"
                placeholder="下界"
                id="open_lo"
                v-model="open_lo"
                required="false"
                style=" width:150px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />~~
            <input
                type="date"
                min="0"
                placeholder="上界"
                id="open_up"
                v-model="open_up"
                required="false"
                style=" width:150px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;最近访问日期
            <input
                type="date"
                min="0"
                placeholder="下界"
                id="visit_lo"
                v-model="visit_lo"
                required="false"
                style=" width:150px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />~~
            <input
                type="date"
                min="0"
                placeholder="上界"
                id="visit_up"
                v-model="visit_up"
                required="false"
                style=" width:150px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;

            <el-button class="button" size="small" type="primary" @click="submit()">查询</el-button>
            <el-button class="button" size="small" type="primary" @click="reset()">重置</el-button>
        </div>
        <br />
        <div align="left">
            <el-button class="button" type="success" size="small" @click="exportCsvEvent()">导出</el-button>
            <el-button class="button" type="success" size="small" @click="insertEvent()">开户</el-button>
        </div>
        <br /><br />
        <elx-editable
            ref="elxEditable"
            class="table"
            border
            :data.sync="list"
            :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod }"
            style="width: 100%"
        >
            <elx-editable-column type="index" width="55"></elx-editable-column>
            <elx-editable-column prop="ID" label="账户号"></elx-editable-column>
            <elx-editable-column prop="owner" label="户主"></elx-editable-column>
            <elx-editable-column prop="bank" label="开户银行" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="money" label="余额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
            <elx-editable-column
                prop="open_date"
                label="开户日期"
                :edit-render="{
                    name: 'ElDatePicker',
                    props: { type: 'date', format: 'yyyy-MM-dd' }
                }"
            ></elx-editable-column>
            <elx-editable-column
                prop="visit_date"
                label="最近访问日期"
                :edit-render="{
                    name: 'ElDatePicker',
                    props: { type: 'date', format: 'yyyy-MM-dd' }
                }"
            ></elx-editable-column>
            <elx-editable-column prop="type" label="账户类型" :edit-render="{ name: 'ElSelect', options: typeList }"></elx-editable-column>
            <elx-editable-column prop="interest" label="利率" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
            <elx-editable-column prop="cashtype" label="货币类型" :edit-render="{ name: 'ElSelect', options: cashList }"></elx-editable-column>
            <elx-editable-column prop="overdraft" label="透支额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
            <elx-editable-column label="操作" width="160">
                <template v-slot="scope">
                    <template v-if="$refs.elxEditable.hasActiveRow(scope.row)">
                        <el-button size="small" type="success" @click="saveRowEvent(scope.row)">保存</el-button>
                        <el-button size="small" type="warning" @click="cancelRowEvent(scope.row)">取消</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="primary" @click="openActiveRowEvent(scope.row)">修改</el-button>
                        <el-button size="small" type="danger" @click="removeEvent(scope.row)">销户</el-button>
                        <el-button size="small" type="primary" @click="updateOwner(scope.row)">更改户主</el-button>
                    </template>
                </template>
            </elx-editable-column>
        </elx-editable>
        <div v-model="primary"></div>
    </div>
</template>

<script>
import XEUtils from "xe-utils";
import XEAjax from "xe-ajax";
import { MessageBox, Message } from "element-ui";
export default {
    data() {
        return {
            loading: false,
            list: [],
            typeList: [
                {
                    label: "储蓄账户",
                    value: "0"
                },
                {
                    label: "支票账户",
                    value: "1"
                }
            ],
            cashList: [
                {
                    label: "人民币",
                    value: "0"
                },
                {
                    label: "美元",
                    value: "1"
                },
                {
                    label: "欧元",
                    value: "2"
                },
                {
                    label: "日元",
                    value: "3"
                }
            ],
            isClearActiveFlag: true,
            bankSearch: "",
            idSearch: "",
            ownerSearch: "",
            typeSearch: "",
            money_lo: "",
            money_up: "",
            open_lo: "",
            open_up: "",
            visit_lo: "",
            visit_up: "",
            primary: null //全局变量，保存记录修改前的主键。当没有活跃的记录时为null，当新增记录时也为null
        };
    },
    created() {
        this.findList();
        this.typeSearch = "any";
    },
    methods: {
        findList() {
            this.loading = true;
            this.list = [
                {
                    ID: "123000",
                    owner: "张三，李四，王五，马云，刘强东",
                    bank: "合肥支行",
                    money: 2563.0,
                    open_date: new Date("2016-2-20"),
                    visit_date: new Date(),
                    type: "0",
                    interest: 0.023,
                    cashtype: "0",
                    overdraft: null
                }
            ];
            this.loading = false;
        },
        formatterDate(row, column, cellValue, index) {
            return XEUtils.toDateString(cellValue, "yyyy-MM-dd HH:mm:ss");
        },
        clearActiveMethod({ type, row }) {
            return this.isClearActiveFlag && type === "out" ? this.checkOutSave(row) : this.isClearActiveFlag;
        },
        //新增记录
        insertEvent() {
            console.log("insert");
            let activeInfo = this.$refs.elxEditable.getActiveRow();
            //let { insertRecords } = this.$refs.elxEditable.getAllRecords();
            console.log(activeInfo);
            //console.log(insertRecords);
            if (!activeInfo) {
                this.$refs.elxEditable
                    .insert({
                        ID: "new id",
                        owner: "",
                        bank: "",
                        money: 0,
                        open_date: new Date(),
                        visit_date: new Date(),
                        type: "0",
                        interest: null,
                        cashtype: null,
                        overdraft: null
                    })
                    .then(({ row }) => {
                        this.$refs.elxEditable.setActiveRow(row);
                    });
            }
        },
        // 点击表格外面处理
        checkOutSave(row) {
            if (!row.id && this.primary != null) {
                console.log("1");
                this.isClearActiveFlag = false;
                MessageBox.confirm("该数据未保存，请确认操作?", "温馨提示", {
                    distinguishCancelAndClose: true,
                    confirmButtonText: "保存数据",
                    cancelButtonText: "取消修改",
                    type: "warning"
                })
                    .then(action => {
                        this.$refs.elxEditable.clearActive();
                        this.saveRowEvent(row);
                    })
                    .catch(action => {
                        if (action === "cancel") {
                            this.$refs.elxEditable.revert(row);
                            this.$refs.elxEditable.clearActive();
                        }
                    })
                    .then(() => {
                        this.isClearActiveFlag = true;
                    });
            } else if (!row.id && this.primary == null) {
                this.isClearActiveFlag = false;
                MessageBox.confirm("该数据未保存，请确认操作?", "温馨提示", {
                    distinguishCancelAndClose: true,
                    confirmButtonText: "保存数据",
                    cancelButtonText: "删除数据",
                    type: "warning"
                })
                    .then(action => {
                        this.$refs.elxEditable.clearActive();
                        this.saveRowEvent(row);
                    })
                    .catch(action => {
                        if (action === "cancel") {
                            this.$refs.elxEditable.remove(row);
                        }
                    })
                    .then(() => {
                        this.isClearActiveFlag = true;
                    });
            }
            return this.isClearActiveFlag;
        },
        // 编辑处理
        openActiveRowEvent(row) {
            this.$nextTick(() => {
                let activeInfo = this.$refs.elxEditable.getActiveRow();
                if (activeInfo && activeInfo.isUpdate) {
                    this.isClearActiveFlag = false;
                    MessageBox.confirm("检测到未保存的内容，请确认操作?", "温馨提示", {
                        distinguishCancelAndClose: true,
                        confirmButtonText: "保存数据",
                        cancelButtonText: "取消修改",
                        type: "warning"
                    })
                        .then(() => {
                            this.$refs.elxEditable.setActiveRow(row);
                            this.primary = row.ID;
                            //console.log(row.name);
                            this.saveRowEvent(activeInfo.row);
                        })
                        .catch(action => {
                            if (action === "cancel") {
                                this.$refs.elxEditable.revert(activeInfo.row);
                                this.$refs.elxEditable.setActiveRow(row);
                            }
                        })
                        .then(() => {
                            this.isClearActiveFlag = true;
                        });
                } else {
                    this.$refs.elxEditable.setActiveRow(row);
                    this.primary = row.ID;
                    console.log(row.ID);
                }
            });
        },
        // 取消处理
        cancelRowEvent(row) {
            if (!row.id) {
                this.isClearActiveFlag = false;
                MessageBox.confirm("该数据未保存，是否移除?", "温馨提示", {
                    distinguishCancelAndClose: true,
                    confirmButtonText: "移除数据",
                    cancelButtonText: "返回继续",
                    type: "warning"
                })
                    .then(action => {
                        if (action === "confirm") {
                            this.$refs.elxEditable.remove(row);
                        }
                    })
                    .catch(action => action)
                    .then(() => {
                        this.isClearActiveFlag = true;
                    });
            } else if (this.$refs.elxEditable.hasRowChange(row)) {
                this.isClearActiveFlag = false;
                MessageBox.confirm("检测到未保存的内容，是否取消修改?", "温馨提示", {
                    distinguishCancelAndClose: true,
                    confirmButtonText: "取消修改",
                    cancelButtonText: "返回继续",
                    type: "warning"
                })
                    .then(action => {
                        this.$refs.elxEditable.clearActive();
                        this.$refs.elxEditable.revert(row);
                    })
                    .catch(action => {
                        if (action === "cancel") {
                            this.$refs.elxEditable.setActiveRow(row);
                        }
                    })
                    .then(() => {
                        this.isClearActiveFlag = true;
                    });
            } else {
                this.$refs.elxEditable.clearActive();
            }
        },
        //删除某一行
        removeEvent(row) {
            this.$http
                .post(
                    "http://" + document.domain + ":5000/account",
                    {
                        type: "Delete",
                        primary: row.ID
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.$refs.elxEditable.remove(row);
                        console.log("Delete");
                    } else {
                        window.alert("删除失败");
                    }
                });
        },
        //保存对某一行的修改
        saveRowEvent(row) {
            this.$refs.elxEditable.validateRow(row, valid => {
                if (valid && this.$refs.elxEditable.hasRowChange(row)) {
                    //数据发生了修改，需要反馈给服务器
                    this.$http
                        .post(
                            "http://" + document.domain + ":5000/account",
                            {
                                type: "Update",
                                ID: row.ID,
                                bank: row.bank,
                                money: row.money,
                                open_date: row.open_date,
                                visit_date: row.visit_date,
                                acctype: row.type,
                                interest: row.interest,
                                cashtype: row.cashtype,
                                overdraft: row.overdraft,
                                old_primary: this.primary //null代表新增
                            },
                            {
                                emulateJSON: true
                            }
                        )
                        .then(function(response) {
                            if (parseInt(response.body.code) === 200) {
                                //更新合法
                                if (row.type === "0") {
                                    row.overdraft = null;
                                } else {
                                    row.cashtype = null;
                                    row.interest = null;
                                }
                                this.primary = null;
                                this.$refs.elxEditable.clearActive();
                                this.$refs.elxEditable.reloadRow(row);
                                console.log("Update");
                            } else {
                                window.alert("更新非法");
                            }
                        });
                } else if (valid && !this.$refs.elxEditable.hasRowChange(row)) {
                    //数据没有修改，不需要向服务器反馈
                    this.primary = null;
                    this.$refs.elxEditable.clearActive();
                }
            });
        },
        //导出CSV
        exportCsvEvent() {
            this.$refs.elxEditable.exportCsv();
        },
        //提交查询请求
        submit() {
            this.$http
                .post(
                    "http://" + document.domain + ":5000/account",
                    {
                        type: "Search",
                        nameSearch: this.nameSearch,
                        idSearch: this.idSearch,
                        ownerSearch: this.ownerSearch,
                        typeSearch: this.typeSearch,
                        money_lo: this.money_lo,
                        money_up: this.money_up,
                        open_lo: this.open_lo,
                        open_up: this.open_up,
                        visit_lo: this.visit_lo,
                        visit_up: this.visit_up
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.list = response.body.list;
                    } else {
                        window.alert("查询失败");
                    }
                });
        },
        //清空查询栏
        reset() {
            this.bankSearch = "";
            this.idSearch = "";
            this.ownerSearch = "";
            this.typeSearch = "any";
            this.money_lo = "";
            this.money_up = "";
            this.open_lo = "";
            this.open_up = "";
            this.visit_lo = "";
            this.visit_up = "";
        },
        updateOwner(row) {}
    }
};
</script>

<style>
.table {
    border: 2px solid #429fff; /* 表格边框 */
    font-family: "汉仪南宫体简";
    font-size: 18px;
    border-collapse: collapse; /* 边框重叠 */
}
.table tr:hover {
    background-color: #c4e4ff; /* 动态变色,IE6下无效！*/
}
.table caption {
    padding-top: 3px;
    padding-bottom: 2px;
    font: bold 1.1em;
    color: #ff00ff;
    background-color: #f0f7ff;
    border: 1px solid #429fff; /* 表格标题边框 */
}
.table th {
    border: 1px solid #429fff; /* 行、列名称边框 */
    background-color: #d2e8ff;
    font-weight: bold;
    padding-top: 4px;
    padding-bottom: 4px;
    padding-left: 10px;
    padding-right: 10px;
    text-align: center;
}
.table td {
    border: 1px solid #429fff; /* 单元格边框 */
    text-align: center;
    padding: 4px;
    word-break: break-all;
}
.button {
    display: inline-block;
    border-radius: 4px;
    background-color: limegreen;
    border: none;
    color: #ffffff;
    text-align: center;
    font-size: 15px;
    padding: 5px;
    width: 80px;
    transition: all 0.5s;
    cursor: pointer;
    margin: 5px;
}
</style>
