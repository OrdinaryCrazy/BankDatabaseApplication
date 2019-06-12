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
            />&emsp;所在部门
            <input
                type="text"
                placeholder="包含关键字"
                id="deptSearch"
                v-model="deptSearch"
                required="false"
                style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;电话号码
            <input
                type="text"
                placeholder="包含关键字"
                id="telSearch"
                v-model="telSearch"
                required="false"
                style=" width:280px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;<br />家庭住址
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
            <el-button class="button" type="success" size="small" @click="insertEvent()">新增</el-button>
            <el-button class="button" type="success" size="small" @click="exportCsvEvent()">导出</el-button>
        </div>
        <br />
        <elx-editable
            ref="elxEditable"
            class="table"
            border
            :data.sync="list"
            :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod }"
            style="width: 100%"
        >
            <elx-editable-column type="index" width="55"></elx-editable-column>
            <elx-editable-column prop="ID" label="身份证号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="name" label="姓名" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="dept" label="所在部门" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="tel" label="电话号码" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="addr" label="家庭住址" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column
                prop="date"
                label="入职日期"
                :edit-render="{
                    name: 'ElDatePicker',
                    props: { type: 'date', format: 'yyyy-MM-dd' }
                }"
            ></elx-editable-column>
            <elx-editable-column label="操作" width="160">
                <template v-slot="scope">
                    <template v-if="$refs.elxEditable.hasActiveRow(scope.row)">
                        <el-button size="small" type="success" @click="saveRowEvent(scope.row)">保存</el-button>
                        <el-button size="small" type="warning" @click="cancelRowEvent(scope.row)">取消</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="primary" @click="openActiveRowEvent(scope.row)">编辑</el-button>
                        <el-button size="small" type="danger" @click="removeEvent(scope.row)">删除</el-button>
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
            <elx-editable
                ref="elxEditable1"
                class="table"
                border
                :data.sync="linklist"
                :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod }"
                style="width: 100%"
            >
                <elx-editable-column type="index" width="55"></elx-editable-column>
                <elx-editable-column prop="ID" label="客户身份证号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
                <elx-editable-column prop="ID" label="客户身份证号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
                <elx-editable-column prop="name" label="客户姓名" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
                <elx-editable-column prop="type" label="与客户关系" :edit-render="{ name: 'ElSelect', options: serviceList }"></elx-editable-column>
                <elx-editable-column label="操作" width="160">
                    <template v-slot="newscope">
                        <template v-if="$refs.elxEditable1.hasActiveRow(newscope.row)">
                            <el-button size="small" type="success" @click="saveRowEvent1(newscope.row)">保存</el-button>
                            <el-button size="small" type="warning" @click="cancelRowEvent1(newscope.row)">取消</el-button>
                        </template>
                        <template v-else>
                            <el-button size="small" type="primary" @click="openActiveRowEvent1(newscope.row)">编辑</el-button>
                            <el-button size="small" type="danger" @click="removeEvent1(newscope.row)">删除</el-button>
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
            deptSearch: "",
            telSearch: "",
            addrSearch: "",
            lowerBound: "",
            upperBound: "",
            showlink: false,
            primary: null //全局变量，保存记录修改前的主键。当没有活跃的记录时为null，当新增记录时也为null
        };
    },
    created() {
        this.findList();
    },
    methods: {
        findList() {
            this.loading = true;
            this.list = [
                {
                    ID: "33122220001010001X",
                    name: "张三",
                    dept: "人事处",
                    tel: "13822100086",
                    addr: "合肥浣纱路256号",
                    date: new Date("2018-2-2")
                }
            ];
            this.linklist = [
                {
                    ID: "33122212121210001X",
                    name: "吴邪",
                    type: "1"
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
        insertEvent(name) {
            console.log("insert");
            let activeInfo = this.$refs.elxEditable.getActiveRow();
            //let { insertRecords } = this.$refs.elxEditable.getAllRecords();
            console.log(activeInfo);
            //console.log(insertRecords);
            if (!activeInfo) {
                this.$refs.elxEditable
                    .insert({
                        ID: "new id",
                        name: "",
                        dept: "",
                        tel: "",
                        addr: "",
                        date: null
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
        // 编辑处理联系表
        openActiveRowEvent1(row) {
            this.$nextTick(() => {
                let activeInfo = this.$refs.elxEditable1.getActiveRow();
                if (activeInfo && activeInfo.isUpdate) {
                    this.isClearActiveFlag = false;
                    MessageBox.confirm("检测到未保存的内容，请确认操作?", "温馨提示", {
                        distinguishCancelAndClose: true,
                        confirmButtonText: "保存数据",
                        cancelButtonText: "取消修改",
                        type: "warning"
                    })
                        .then(() => {
                            this.$refs.elxEditable1.setActiveRow(row);
                            this.primary = row.ID;
                            //console.log(row.name);
                            this.saveRowEvent(activeInfo.row);
                        })
                        .catch(action => {
                            if (action === "cancel") {
                                this.$refs.elxEditable1.revert(activeInfo.row);
                                this.$refs.elxEditable1.setActiveRow(row);
                            }
                        })
                        .then(() => {
                            this.isClearActiveFlag = true;
                        });
                } else {
                    this.$refs.elxEditable1.setActiveRow(row);
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
                    "http://" + document.domain + ":5000/staff",
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
                            "http://" + document.domain + ":5000/staff",
                            {
                                type: "Update",
                                ID: row.ID,
                                name: row.name,
                                dept: row.dept,
                                tel: row.tel,
                                addr: row.addr,
                                date: row.date,
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
                                this.$refs.elxEditable.clearActive();
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
        //保存对联系表中某一行的修改
        saveRowEvent1(row) {
            this.$refs.elxEditable1.validateRow(row, valid => {
                if (valid && this.$refs.elxEditable1.hasRowChange(row)) {
                    //数据发生了修改，需要反馈给服务器
                    this.$http
                        .post(
                            "http://" + document.domain + ":5000/staff",
                            {
                                type: "Update",
                                ID: row.ID,
                                name: row.name,
                                dept: row.dept,
                                tel: row.tel,
                                addr: row.addr,
                                date: row.date,
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
                                this.$refs.elxEditable.clearActive();
                                console.log("Update");
                            } else {
                                window.alert("更新非法");
                            }
                        });
                } else if (valid && !this.$refs.elxEditable1.hasRowChange(row)) {
                    //数据没有修改，不需要向服务器反馈
                    this.primary = null;
                    this.$refs.elxEditable1.clearActive();
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
                    "http://" + document.domain + ":5000/staff",
                    {
                        type: "Search",
                        nameSearch: this.nameSearch,
                        idSearch: this.idSearch,
                        deptSearch: this.deptSearch,
                        telSearch: this.telSearch,
                        addrSearch: this.addrSearch,
                        lowerBound: this.lowerBound,
                        upperBound: this.upperBound
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
        },

        
    }
};
</script>

<style>
.table {
    border: 2px solid #429fff; /* 表格边框 */
    font-family: "汉仪南宫体简";
    font-size: 18px;
    max-height: 500px;
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
