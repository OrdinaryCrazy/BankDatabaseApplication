<template>
    <div v-loading="loading">
        <h1>员工管理</h1>
        <p style="color: red;font-size: 24px;" align="left">条件筛选</p>
        <div align="left">
            身份证号
            <input
                type="text"
                placeholder="包含关键字"
                id="idSearch"
                v-model="idSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;姓名
            <input
                type="text"
                placeholder="包含关键字"
                id="nameSearch"
                v-model="nameSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;所属支行
            <input
                type="text"
                placeholder="包含关键字"
                id="bankSearch"
                v-model="bankSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;所在部门
            <input
                type="text"
                placeholder="包含关键字"
                id="deptSearch"
                v-model="deptSearch"
                required="false"
                style=" width:280px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;<br />电话号码
            <input
                type="text"
                placeholder="包含关键字"
                id="telSearch"
                v-model="telSearch"
                required="false"
                style=" width:280px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;家庭住址
            <input
                type="text"
                placeholder="包含关键字"
                id="addrSearch"
                v-model="addrSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;入职日期
            <input
                type="date"
                placeholder="下界"
                id="lowerBound"
                v-model="lowerBound"
                required="false"
                style="   width:200px;
                    font-family: 'Fira Code', '汉仪南宫体简';
                "
            />~~
            <input
                type="date"
                placeholder="上界"
                id="upperBound"
                v-model="upperBound"
                required="false"
                style=" width:200px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;
            <el-button class="button" size="small" type="primary" @click="submit()">查询</el-button>
            <el-button class="button" size="small" type="primary" @click="reset()">重置</el-button>
        </div>
        <br />
        <p style="color: red;font-size: 24px;" align="left">员工信息表</p>
        <div align="left">
            <el-button class="button" type="success" size="small" @click="insertEvent('elxEditable1')">新增</el-button>
            <el-button class="button" type="success" size="small" @click="exportCsvEvent('elxEditable1')">导出</el-button>
        </div>
        <br />
        <elx-editable
            ref="elxEditable1"
            class="table"
            border
            :data.sync="list"
            :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod: clearActiveMethod1 }"
            style="width: 100%"
        >
            <elx-editable-column type="index" width="55"></elx-editable-column>
            <elx-editable-column prop="id" label="身份证号" min-width="100" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="name" label="姓名" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="bank" label="所属支行" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="dept" label="所在部门" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="tel" label="电话号码" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="addr" label="家庭住址" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column
                prop="date_s"
                label="入职日期"
                :edit-render="{
                    name: 'ElDatePicker',
                    props: { type: 'date', format: 'yyyy-MM-dd' }
                }"
            ></elx-editable-column>
            <elx-editable-column label="操作" width="160">
                <template v-slot="scope">
                    <template v-if="$refs.elxEditable1.hasActiveRow(scope.row)">
                        <el-button size="small" type="success" @click="saveRowEvent('elxEditable1', scope.row)">保存</el-button>
                        <el-button size="small" type="warning" @click="cancelRowEvent('elxEditable1', scope.row)">取消</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="primary" @click="openActiveRowEvent('elxEditable1', scope.row)">编辑</el-button>
                        <el-button size="small" type="danger" @click="removeEvent('elxEditable1', scope.row)">删除</el-button>
                        <el-button size="small" type="danger" @click="showDetail(scope.row)">详情</el-button>
                    </template>
                </template>
            </elx-editable-column>
        </elx-editable>
        <div v-if="showlink">
            <br />
            <p style="color: red;font-size: 24px;" align="left">
                客户联系表
                <el-button class="button" type="success" size="small" @click="showlink = false">关闭</el-button>
            </p>
            <div align="left">
                <el-button class="button" type="success" size="small" @click="insertEvent('elxEditable2')">新增</el-button>
                <el-button class="button" type="success" size="small" @click="exportCsvEvent('elxEditable2')">导出</el-button>
            </div>
            <br />
            <elx-editable
                ref="elxEditable2"
                class="table"
                border
                :data.sync="linklist"
                :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod: clearActiveMethod2 }"
                style="width: 100%"
            >
                <elx-editable-column type="index" width="55"></elx-editable-column>
                <elx-editable-column prop="staffID" label="员工身份证号"></elx-editable-column>
                <elx-editable-column prop="staffName" label="员工姓名"></elx-editable-column>
                <elx-editable-column prop="id" label="客户身份证号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
                <elx-editable-column prop="name" label="客户姓名"></elx-editable-column>
                <!-- <elx-editable-column prop="type" label="与客户关系" :edit-render="{ name: 'ElSelect', options: serviceList }"></elx-editable-column> -->
                <elx-editable-column prop="type" label="与客户关系" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
                <elx-editable-column label="操作" width="160">
                    <template v-slot="newscope">
                        <template v-if="$refs.elxEditable2.hasActiveRow(newscope.row)">
                            <el-button size="small" type="success" @click="saveRowEvent('elxEditable2', newscope.row)">保存</el-button>
                            <el-button size="small" type="warning" @click="cancelRowEvent('elxEditable2', newscope.row)">取消</el-button>
                        </template>
                        <template v-else>
                            <el-button size="small" type="primary" @click="openActiveRowEvent('elxEditable2', newscope.row)">编辑</el-button>
                            <el-button size="small" type="danger" @click="removeEvent('elxEditable2', newscope.row)">删除</el-button>
                        </template>
                    </template>
                </elx-editable-column>
            </elx-editable>
        </div>
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
            linklist: [],
            serviceList: [
                {
                    label: "银行账户负责人",
                    value: "0"
                },
                {
                    label: "贷款负责人",
                    value: "1"
                }
            ],
            isClearActiveFlag: true,
            nameSearch: "",
            idSearch: "",
            bankSearch: "",
            deptSearch: "",
            telSearch: "",
            addrSearch: "",
            lowerBound: "",
            upperBound: "",
            showlink: false,
            detail: "",
            detailName: "",
            permission: "",
            primary: null //全局变量，保存记录修改前的主键。当没有活跃的记录时为null，当新增记录时也为null
        };
    },
    created() {
        this.permission = localStorage.getItem("type");
        if (this.permission != "SUB_BANK" && this.permission != "EMPLOYEE") {
            this.$router.push("/404");
        }
        this.findList();
    },
    methods: {
        findList() {
            this.loading = true;
            this.list = [
                // {
                //     id: "33122220001010001X",
                //     name: "张三",
                //     bank: "合肥城南支行",
                //     dept: "人事处",
                //     tel: "13822100086",
                //     addr: "合肥浣纱路256号",
                //     date: new Date("2018-2-2")
                // }
            ];
            this.linklist = [
                // {
                //     id: "33122212121210001X",
                //     name: "吴邪",
                //     staffID: "33122220001010001X",
                //     staffName: "张三",
                //     type: "1"
                // }
            ];
            this.loading = false;
        },
        formatterDate(row, column, cellValue, index) {
            return XEUtils.toDateString(cellValue, "yyyy-MM-dd");
        },
        clearActiveMethod1({ type, row, rowIndex }) {
            return this.isClearActiveFlag && type === "out" ? this.checkSaveData("elxEditable1", row) : this.isClearActiveFlag;
        },
        clearActiveMethod2({ type, row, rowIndex }) {
            return this.isClearActiveFlag && type === "out" ? this.checkSaveData("elxEditable2", row) : this.isClearActiveFlag;
        },
        //新增记录
        insertEvent(name) {
            let activeInfo = this.$refs[name].getActiveRow();
            if (!activeInfo) {
                if (name === "elxEditable1") {
                    this.$refs[name].insert().then(({ row }) => {
                        this.$refs[name].setActiveRow(row);
                    });
                } else {
                    this.$refs[name].insert({ staffID: this.detail.id, staffName: this.detail.name }).then(({ row }) => {
                        this.$refs[name].setActiveRow(row);
                    });
                }
            }
        },
        customExportCsvEvent(name, opts) {
            this.$refs[name].exportCsv(opts);
        },

        //提交查询请求
        submit() {
            this.$http
                .post(
                    "http://" + document.domain + ":5000/staff",
                    {
                        type: "Search",
                        nameSearch: this.nameSearch,
                        idSearch: this.idSearch,
                        bankSearch: this.bankSearch,
                        deptSearch: this.deptSearch,
                        telSearch: this.telSearch,
                        addrSearch: this.addrSearch,
                        lowerBound: XEUtils.toDateString(this.lowerBound, "yyyy-MM-dd"),
                        upperBound: XEUtils.toDateString(this.upperBound, "yyyy-MM-dd")
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
            this.nameSearch = "";
            this.idSearch = "";
            this.deptSearch = "";
            this.telSearch = "";
            this.addrSearch = "";
            this.lowerBound = "";
            this.upperBound = "";
        },
        showDetail(row) {
            this.showlink = true;
            this.detail = row;
            this.$http
                .post(
                    "http://" + document.domain + ":5000/staffCustomer",
                    {
                        type: "SearchByStaff",
                        staffID: row.id
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.linklist = response.body.list;
                        for (var i = 0; i < this.linklist.length; i++) {
                            this.linklist[i].staffName = row.name;
                            this.linklist[i].staffID = row.id;
                        }
                    } else {
                        window.alert("查询失败");
                    }
                });
        },

        // 判断多表格切换时是否有数据没有保存
        checkSaveData(name, row) {
            if (this.$refs[name].hasRowChange(row)) {
                this.isClearActiveFlag = false;
                MessageBox.confirm("您离开了表格，检测未保存的内容，是否在离开前保存修改?", "温馨提示", {
                    closeOnClickModal: false,
                    distinguishCancelAndClose: true,
                    confirmButtonText: "保存",
                    cancelButtonText: "放弃修改",
                    type: "warning"
                })
                    .then(() => {
                        this.saveRowEvent(name, row);
                    })
                    .catch(action => {
                        if (action === "cancel") {
                            this.$refs[name].revert(row);
                            this.$refs[name].clearActive();
                            if (this.primary == null) {
                                this.$refs[name].remove(row);
                            }
                            this.primary = null;
                            Message({ message: "放弃修改并离开当前行", type: "warning" });
                        } else {
                            this.$refs[name].setActiveRow(row);
                            Message({ message: "停留在当前行编辑", type: "info" });
                        }
                    })
                    .then(() => {
                        this.isClearActiveFlag = true;
                    });
                return false;
            } else {
                this.primary = null;
            }
            return this.isClearActiveFlag;
        },
        openActiveRowEvent(name, row) {
            this.$nextTick(() => {
                let activeInfo = this.$refs[name].getActiveRow();
                // 如果当前行正在编辑中，禁止编辑其他行
                if (activeInfo) {
                    if (activeInfo.row === row || !this.$refs[name].checkValid().error) {
                        if (activeInfo.isUpdate) {
                            this.isClearActiveFlag = false;
                            MessageBox.confirm("检测到未保存的内容，是否在离开前保存修改?", "温馨提示", {
                                closeOnClickModal: false,
                                distinguishCancelAndClose: true,
                                confirmButtonText: "保存",
                                cancelButtonText: "放弃修改",
                                type: "warning"
                            })
                                .then(() => {
                                    this.$refs[name].setActiveRow(row);
                                    this.primary = row.id;
                                    console.log(row.id);
                                    this.saveRowEvent(name, activeInfo.row);
                                })
                                .catch(action => {
                                    if (action === "cancel") {
                                        this.$refs[name].revert(activeInfo.row);
                                        this.$refs[name].setActiveRow(row);
                                        Message({ message: "放弃修改并离开当前行", type: "warning" });
                                    } else {
                                        Message({ message: "停留在当前行编辑", type: "info" });
                                    }
                                })
                                .then(() => {
                                    this.isClearActiveFlag = true;
                                });
                        } else {
                            this.$refs[name].setActiveRow(row);
                            this.primary = row.id;
                            console.log(row.id);
                        }
                    }
                } else {
                    this.$refs[name].setActiveRow(row);
                    this.primary = row.id;
                    console.log(row.id);
                }
            });
        },
        removeEvent(name, row) {
            switch (name) {
                case "elxEditable1":
                    this.$http
                        .post(
                            "http://" + document.domain + ":5000/staff",
                            {
                                type: "Delete",
                                primary: row.id
                            },
                            {
                                emulateJSON: true
                            }
                        )
                        .then(function(response) {
                            if (parseInt(response.body.code) === 200) {
                                this.$refs.elxEditable1.remove(row);
                                console.log("Delete");
                            } else {
                                window.alert("删除失败");
                            }
                        });
                    break;
                case "elxEditable2":
                    this.userLoading = true;
                    this.$http
                        .post(
                            "http://" + document.domain + ":5000/staffCustomer",
                            {
                                type: "Delete",
                                custID: row.id,
                                staffID: row.staffID
                            },
                            {
                                emulateJSON: true
                            }
                        )
                        .then(function(response) {
                            if (parseInt(response.body.code) === 200) {
                                this.$refs.elxEditable2.remove(row);
                                console.log("Delete");
                            } else {
                                window.alert("删除失败");
                            }
                        });
                    break;
            }
        },
        saveRowEvent(name, row) {
            switch (name) {
                case "elxEditable2":
                    if (row.staffID == null || row.staffID == "") {
                        return;
                    }
                case "elxEditable1":
                    if (row.id == null || row.id == "") {
                        return;
                    }
            }
            console.log(row);
            this.$refs[name].validateRow(row, valid => {
                if (valid && this.$refs[name].hasRowChange(row)) {
                    switch (name) {
                        case "elxEditable1":
                            this.$http
                                .post(
                                    "http://" + document.domain + ":5000/staff",
                                    {
                                        type: "Update",
                                        id: row.id,
                                        name: row.name,
                                        bank: row.bank,
                                        dept: row.dept,
                                        tel: row.tel,
                                        addr: row.addr,
                                        date_s: XEUtils.toDateString(row.date_s, "yyyy-MM-dd"),
                                        old_primary: this.primary //null代表新增
                                    },
                                    {
                                        emulateJSON: true
                                    }
                                )
                                .then(function(response) {
                                    if (parseInt(response.body.code) === 200) {
                                        //更新合法
                                        this.primary = null;
                                        this.$refs.elxEditable1.clearActive();
                                        console.log("Update");
                                        this.$refs.elxEditable1.reloadRow(row);
                                    } else {
                                        window.alert("更新非法");
                                    }
                                });
                            break;
                        case "elxEditable2":
                            this.$http
                                .post(
                                    "http://" + document.domain + ":5000/staffCustomer",
                                    {
                                        type: "Update",
                                        custID: row.id,
                                        staffID: row.staffID, //该字段是不变的
                                        serviceType: row.type,
                                        old_custID: this.primary, //null代表新增，这是旧的客户身份证号
                                        old_staffID: row.staffID
                                    },
                                    {
                                        emulateJSON: true
                                    }
                                )
                                .then(function(response) {
                                    if (parseInt(response.body.code) === 200) {
                                        //更新合法
                                        this.primary = null;
                                        this.$refs.elxEditable2.clearActive();
                                        row = response.body.record;
                                        this.$refs.elxEditable2.reloadRow(row);
                                        console.log("Update");
                                    } else {
                                        window.alert("更新非法");
                                    }
                                });
                            break;
                    }
                } else if (valid) {
                    this.$refs[name].clearActive();
                    this.primary = null;
                }
            });
        },
        cancelRowEvent(name, row) {
            let activeInfo = this.$refs[name].getActiveRow();
            if (activeInfo && activeInfo.isUpdate) {
                this.isClearActiveFlag = false;
                MessageBox.confirm("检测到未保存的内容，确定放弃修改?", "温馨提示", {
                    closeOnClickModal: false,
                    confirmButtonText: "放弃更改",
                    cancelButtonText: "返回",
                    type: "warning"
                })
                    .then(action => {
                        if (action === "confirm") {
                            this.$refs[name].clearActive();
                            this.$refs[name].revert(row);
                            if (this.primary == null) {
                                this.$refs[name].remove(row);
                            }
                            this.primary = null;
                        } else {
                            this.$refs[name].setActiveRow(row);
                        }
                    })
                    .catch(e => e)
                    .then(() => {
                        this.isClearActiveFlag = true;
                    });
            } else {
                this.$refs[name].clearActive();
                this.primary = null;
            }
        }
    }
};
</script>

<style>
.table {
    border: 2px solid #429fff; /* 表格边框 */
    font-family: "汉仪南宫体简";
    font-size: 18px;
    max-height: 500px;
    overflow-x: auto;
    overflow-y: auto;
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
