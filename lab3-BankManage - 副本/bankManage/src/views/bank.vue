<template>
    <div v-loading="loading">
        <h1>支行管理</h1>
        <p style="color: red;font-size: 24px;" align="left">条件筛选</p>
        <div align="left">
            支行名称
            <input
                type="text"
                placeholder="包含关键字"
                class="input"
                id="bankSearch"
                v-model="bankSearch"
                required="false"
                style=" width:250px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;所在城市
            <input
                type="text"
                placeholder="包含关键字"
                class="input"
                id="citySearch"
                v-model="citySearch"
                required="false"
                style=" width:250px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;资产总额
            <input
                type="number"
                min="0"
                placeholder="下界"
                class="input"
                id="lowerBound"
                v-model="lowerBound"
                required="false"
                style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />~~
            <input
                type="number"
                min="0"
                placeholder="上界"
                class="input"
                id="upperBound"
                v-model="upperBound"
                required="false"
                style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;
            <el-button size="small" type="primary" @click="submit()">查询</el-button>
            <el-button size="small" type="primary" @click="reset()">重置</el-button>
        </div>
        <br />
        <p style="color: red;font-size: 24px;" align="left">支行信息表</p>
        <div align="left">
            <el-button type="success" size="small" @click="insertEvent()">新增</el-button>
            <el-button type="success" size="small" @click="exportCsvEvent()">导出</el-button>
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
            <elx-editable-column prop="name" label="支行名称" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="city" label="所在城市" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="money" label="资产总额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
            <elx-editable-column label="操作" width="160">
                <template v-slot="scope">
                    <template v-if="$refs.elxEditable.hasActiveRow(scope.row)">
                        <el-button size="small" type="success" @click="saveRowEvent(scope.row)">保存</el-button>
                        <el-button size="small" type="warning" @click="cancelRowEvent(scope.row)">取消</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="primary" @click="openActiveRowEvent(scope.row)">编辑</el-button>
                        <el-button size="small" type="danger" @click="removeEvent(scope.row)">删除</el-button>
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
            isClearActiveFlag: true,
            bankSearch: "",
            citySearch: "",
            lowerBound: "",
            upperBound: "",
            permission: "",
            primary: null //全局变量，保存记录修改前的主键。当没有活跃的记录时为null，当新增记录时也为null
        };
    },
    created() {
        this.permission = localStorage.getItem("type");
        if (this.permission != "SUB_BANK") {
            this.$router.push("/404");
        }
        this.findList();
    },
    methods: {
        findList() {
            this.loading = true;
            this.list = [];
            this.loading = false;
        },
        formatterDate(row, column, cellValue, index) {
            return XEUtils.toDateString(cellValue, "yyyy-MM-dd HH:mm:ss");
        },
        clearActiveMethod({ type, row }) {
            return false;
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
                        name: "New Bank",
                        city: "",
                        money: 0
                    })
                    .then(({ row }) => {
                        this.$refs.elxEditable.setActiveRow(row);
                    });
            }
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
                            this.primary = row.name;
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
                    this.primary = row.name;
                    console.log(row.name);
                }
            });
        },
        // 取消处理
        cancelRowEvent(row) {
            if (this.primary == null) {
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
                        if (this.primary == null) {
                            this.$refs.elxEditable.remove(row);
                        }
                        this.primary = null;
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
                    "http://" + document.domain + ":5000/bank",
                    {
                        type: "Delete",
                        primary: row.name
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.$refs.elxEditable.remove(row);
                        Message({ message: "删除成功", type: "success" });
                    } else {
                        Message({ message: "删除失败，" + response.body.msg, type: "warning" });
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
                            "http://" + document.domain + ":5000/bank",
                            {
                                type: "Update",
                                name: row.name,
                                city: row.city,
                                money: row.money,
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
                                this.$refs.elxEditable.reloadRow(row);
                                console.log("Update");
                                Message({ message: "保存成功", type: "success" });
                            } else if (parseInt(response.body.code) === 400) {
                                Message({ message: "新增记录失败，可能是支行名称重复", type: "warning" });
                            } else {
                                Message({ message: "更新失败\n" + response.body.msg, type: "warning" });
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
                    "http://" + document.domain + ":5000/bank",
                    {
                        type: "Search",
                        bankSearch: this.bankSearch,
                        citySearch: this.citySearch,
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
                        Message({ message: "查询成功", type: "success" });
                    } else {
                        Message({ message: "没有查到任何内容", type: "warning" });
                    }
                });
        },
        //清空查询栏
        reset() {
            this.bankSearch = "";
            this.citySearch = "";
            this.lowerBound = "";
            this.upperBound = "";
        }
    }
};
</script>

<style>
.input{
    outline-style: none ;
    border: 1px solid #ccc; 
    border-radius: 6px;
    padding: 8px 14px;
    width: 620px;
    font-size: 14px;
    font-weight: 700;
    font-family: "Fira Code", "汉仪南宫体简";
}
.input:focus{
    border-color: #66afe9;
    outline: 0;
    -webkit-box-shadow: inset 0 3px 3px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6);
    box-shadow: inset 0 3px 3px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6)
}
</style>
