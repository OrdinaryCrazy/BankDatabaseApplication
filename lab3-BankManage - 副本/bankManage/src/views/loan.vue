<template>
    <div v-loading="loading">
        <h1>贷款管理</h1>
        <p style="color: red;font-size: 24px;" align="left">条件筛选</p>
        <div align="left">
            贷款号
            <input
                type="text"
                placeholder="包含关键字"
                id="idSearch"
                v-model="idSearch"
                required="false"
                class="input"
                style=" width:220px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;放款支行
            <input
                type="text"
                placeholder="包含关键字"
                id="bankSearch"
                v-model="bankSearch"
                class="input"
                required="false"
                style=" width:220px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;贷款人
            <input
                type="text"
                placeholder="包含关键字"
                id="custSearch"
                v-model="custSearch"
                class="input"
                required="false"
                style=" width:220px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;状态
            <select class="dropbtn" v-model="statusSearch" id="statusSearch">
                <option value="any" selected>任意</option>
                <option value="none">未开始发放</option>
                <option value="part">发放中</option>
                <option value="all">已全部发放</option> </select
            ><br /><br />金额
            <input
                type="number"
                min="0"
                placeholder="下界"
                id="lowerBound"
                v-model="lowerBound"
                class="input"
                required="false"
                style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />~~
            <input
                type="number"
                min="0"
                placeholder="上界"
                id="upperBound"
                v-model="upperBound"
                class="input"
                required="false"
                style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;

            <el-button size="small" type="primary" @click="submit()">查询</el-button>
            <el-button size="small" type="primary" @click="reset()">重置</el-button>
        </div>
        <br />
        <p style="color: red;font-size: 24px;" align="left">贷款信息表</p>
        <div align="left">
            <el-button type="success" size="small" @click="exportCsvEvent()">导出</el-button>
            <el-button type="success" size="small" @click="insertEvent()">发放贷款</el-button>
            <font style="color: red" align="left" v-if="messageshow">请在贷款人字段填写所有贷款人的身份证号，并使用英文逗号分隔</font>
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
            <elx-editable-column prop="id" label="贷款号" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="bank" label="放款支行" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="customer" label="贷款人" :edit-render="{ name: 'ElInput' }"></elx-editable-column>
            <elx-editable-column prop="amount" label="金额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
            <elx-editable-column prop="status" label="状态"></elx-editable-column>
            <elx-editable-column label="操作" width="260">
                <template v-slot="scope">
                    <template v-if="$refs.elxEditable.hasActiveRow(scope.row)">
                        <el-button size="small" type="success" @click="saveRowEvent(scope.row)">保存</el-button>
                        <el-button size="small" type="warning" @click="cancelRowEvent(scope.row)">取消</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="danger" @click="removeEvent(scope.row)">删除</el-button>
                        <el-button size="small" type="success" @click="showDetail(scope.row)">详情</el-button>
                    </template>
                </template>
            </elx-editable-column>
        </elx-editable>
        <div v-if="showlink">
            <p style="color: red;font-size: 24px;" align="left">
                支付信息表
                <el-button type="success" size="small" @click="showlink = false">关闭</el-button>
            </p>
            <div align="left">
                进行支付&emsp;
                <input
                    type="number"
                    min="0"
                    placeholder="金额"
                    id="payAmount"
                    v-model="payAmount"
                    required="false"
                    style=" width:100px;font-family: 'Fira Code', '汉仪南宫体简';"
                />
                <el-button type="success" size="small" @click="newpay()">支付</el-button><br /><br />
            </div>
            <elx-table ref="elxTable" border size="small" :data.sync="paylist" style="width: 100%" class="table">
                <elx-table-column type="index" width="55"></elx-table-column>
                <elx-table-column prop="id" label="贷款号"></elx-table-column>
                <elx-table-column prop="date_s" label="支付日期" :formatter="formatterDate"></elx-table-column>
                <elx-table-column prop="money" label="支付金额"></elx-table-column>
            </elx-table>
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
            statusList: ["未开始发放", "发放中", "已全部发放"],
            paylist: [],
            showlink: false,
            showpay: false,
            isClearActiveFlag: true,
            bankSearch: "",
            idSearch: "",
            statusSearch: "any",
            custSearch: "",
            upperBound: "",
            lowerBound: "",
            detail: "",
            payAmount: "",
            messageshow: false,
            permission: "",
            primary: null //全局变量，保存记录修改前的主键。当没有活跃的记录时为null，当新增记录时也为null
        };
    },
    created() {
        this.permission = localStorage.getItem("type");
        if (type != "EMPLOYEE" && type != "SUB_BANK" && type != "CUSTOMER") {
            this.$router.push("/404");
        }
        this.findList();
        this.statusSearch = "any";
    },
    methods: {
        findList() {
            this.loading = true;
            this.list = [
                {
                    id: "2019031145",
                    bank: "合肥城南支行",
                    customer: "10002 王三云\n10005 张无忌",
                    amount: 500000,
                    status: "未开始发放"
                }
            ];
            this.loading = false;
        },
        formatterDate(row, column, cellValue, index) {
            return XEUtils.toDateString(cellValue, "yyyy-MM-dd");
        },
        clearActiveMethod({ type, row }) {
            return false;
        },
        showDetail(row) {
            this.showlink = true;
            this.detail = row;
            this.$http
                .post(
                    "http://" + document.domain + ":5000/pay",
                    {
                        type: "Search",
                        loanid: row.id
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.paylist = response.body.list;
                        for (var i = 0; i < this.paylist.length; i++) {
                            this.paylist[i].id = row.id;
                        }
                        Message({ message: "查询成功", type: "success" });
                    } else {
                        Message({ message: "查询结果为空", type: "warning" });
                        this.paylist=[];
                    }
                });
        },
        newpay() {
            if (this.payAmount == "") {
                Message({ message: "支付金额不能为空", type: "warning" });
                return;
            }
            var sum = parseInt(this.payAmount);
            for (var i = 0; i < this.paylist.length; i++) {
                sum = sum +  parseInt(this.paylist[i].money);
            }
            console.log(sum);
            if (sum > this.detail.amount) {
                Message({ message: "支付超额", type: "warning" });
                return;
            }
            this.$http
                .post(
                    "http://" + document.domain + ":5000/pay",
                    {
                        type: "Insert",
                        loanid: this.detail.id,
                        date: XEUtils.toDateString(new Date(), "yyyy-MM-dd"),
                        money: this.payAmount
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.paylist.push({ id: this.detail.id, date_s: XEUtils.toDateString(new Date(), "yyyy-MM-dd"), money: this.payAmount });
                        var sum = 0;
                        for (var i = 0; i < this.paylist.length; i++) {
                            sum = sum + parseInt(this.paylist[i].money);
                        }
                        if (sum < this.detail.amount) {
                            this.detail.status = "发放中";
                        } else if (sum == 0) {
                            this.detail.status = "未开始发放";
                        } else {
                            this.detail.status = "已全部发放";
                        }
                        Message({ message: "支付成功", type: "success" });
                    } else {
                        Message({ message: "支付失败，可能超额", type: "warning" });
                    }
                });
        },
        //新增记录
        insertEvent() {
            console.log("insert");
            this.messageshow = true;
            let activeInfo = this.$refs.elxEditable.getActiveRow();
            //let { insertRecords } = this.$refs.elxEditable.getAllRecords();
            console.log(activeInfo);
            //console.log(insertRecords);
            if (!activeInfo) {
                this.$refs.elxEditable
                    .insert({
                        id: "new id",
                        bank: "",
                        customer: "",
                        amount: 0,
                        status: "未开始发放"
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
                            this.primary = row.id;
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
                    this.primary = row.id;
                    console.log(row.id);
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
                            this.messageshow = false;
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
            if (row.status == "发放中") {
                Message({ message: "发放中的贷款不能删除", type: "warning" });
                return;
            }
            this.$http
                .post(
                    "http://" + document.domain + ":5000/loan",
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
                        this.$refs.elxEditable.remove(row);
                        Message({ message: "删除成功", type: "success" });
                    } else {
                        Message({ message: "发放中的贷款不能删除", type: "warning" });
                    }
                });
        },
        //保存对某一行的修改
        saveRowEvent(row) {
            console.log("save");
            console.log(row);
            if (row.id == "" || row.bank == "" || row.customer == "" || row.amount < 0) {
                Message({ message: "字段不能为空", type: "warning" });
                return;
            }
            this.messageshow = false;
            this.$refs.elxEditable.validateRow(row, valid => {
                if (valid && this.$refs.elxEditable.hasRowChange(row)) {
                    //数据发生了修改，需要反馈给服务器
                    this.$http
                        .post(
                            "http://" + document.domain + ":5000/loan",
                            {
                                type: "Update",
                                id: row.id,
                                bank: row.bank,
                                customer: row.customer,
                                amount: row.amount,
                                status: this.statusList.indexOf(row.status),
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
                                row.customer = response.body.customer; //从后端得到所有贷款人的名字
                                this.$refs.elxEditable.clearActive();
                                this.$refs.elxEditable.reloadRow(row);
                                Message({ message: "发放贷款成功", type: "success" });
                            } else {
                                Message({ message: "发放贷款失败,可能是输入信息错误", type: "warning" });
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
                    "http://" + document.domain + ":5000/loan",
                    {
                        type: "Search",
                        idSearch: this.idSearch,
                        bankSearch: this.bankSearch,
                        statusSearch: this.statusSearch,
                        custSearch: this.custSearch,
                        upperBound: this.upperBound,
                        lowerBound: this.lowerBound
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.list = response.body.list;
                        for (var i = 0; i < this.list.length; i++) {
                            var t = this.list[i].status;
                            this.list[i].status = this.statusList[t];
                        }
                        this.showlink = false;
                        Message({ message: "查询成功", type: "success" });
                    } else {
                        this.showlink = false;
                        Message({ message: "查询结果为空", type: "warning" });
                    }
                });
        },
        //清空查询栏
        reset() {
            this.bankSearch = "";
            this.idSearch = "";
            this.statusSearch = "any";
            this.custSearch = "";
            this.upperBound = "";
            this.lowerBound = "";
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
.dropbtn {
    border-radius: 6px;
    background-color: rgb(223, 71, 71);
    color: white;
    padding: 8px;
    font-size: 14px;
    border: none;
    cursor: pointer;
    width: 120px;
    height: 35px;
    font-family: "Fira Code", "汉仪南宫体简";
}

.dropdown {
    position: relative;
    border-radius: 4px;
    display: inline-block;
}

.dropdown-content {
    border-radius: 4px;
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
}

.dropdown-content option {
    color: black;
    padding: 6px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content option :hover {background-color: #f1f1f1}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown:hover .dropbtn {
    background-color: #b6f699;
}
</style>
