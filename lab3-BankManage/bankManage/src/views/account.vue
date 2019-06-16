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
                class="input"
                required="false"
                style=" width:250px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;户主
            <input
                type="text"
                placeholder="包含关键字"
                id="ownerSearch"
                v-model="ownerSearch"
                class="input"
                required="false"
                style=" width:250px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;开户银行
            <input
                type="text"
                placeholder="包含关键字"
                id="bankSearch"
                v-model="bankSearch"
                required="false"
                class="input"
                style=" width:250px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;账户类型
            <select class="dropbtn" v-model="typeSearch" id="typeSearch" placeholder="any">
                <option value="any" selected>任意</option>
                <option value="saving">储蓄账户</option>
                <option value="check">支票账户</option> </select
            ><br /><br />余额
            <input
                type="number"
                min="0"
                placeholder="下界"
                id="money_lo"
                class="input"
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
                class="input"
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
                class="input"
                required="false"
                style=" width:150px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />~~
            <input
                type="date"
                min="0"
                placeholder="上界"
                class="input"
                id="open_up"
                v-model="open_up"
                required="false"
                style=" width:150px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            /><!-- &emsp;最近访问日期
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
            />&emsp; -->

            <el-button size="small" type="primary" @click="submit()">查询</el-button>
            <el-button size="small" type="primary" @click="reset()">重置</el-button>
        </div>
        <br />
        <p style="color: red;font-size: 24px;" align="left">
            账户信息表 <el-button type="success" size="small" @click="exportCsvEvent()">导出</el-button>
        </p>

        <div align="left">
            开户者
            <input
                type="text"
                placeholder="身份证号"
                class="input"
                id="newownerid"
                v-model="newownerid"
                style=" width:220px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;账户号
            <input
                type="text"
                placeholder="账户号"
                id="newbankid"
                class="input"
                v-model="newbankid"
                style=" width:220px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp;开户支行
            <input
                type="text"
                placeholder="支行名称"
                id="newbankname"
                v-model="newbankname"
                class="input"
                style=" width:220px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
            />&emsp; <br/><br/>账户类型
            <select class="dropbtn" v-model="newtype">
                <option value="0">储蓄账户</option>
                <option value="1">支票账户</option> </select
            >&emsp;
            <label v-if="newtype == '0'"> 货币类型 </label>
            <select class="dropbtn" v-model="newmoneytype" v-if="newtype == '0'">
                <option value="0">人民币</option>
                <option value="1">美元</option>
                <option value="2">欧元</option>
                <option value="3">日元</option> </select
            >&emsp;

            <el-button type="success" size="small" @click="newaccount()">开户</el-button>
            <el-button type="success" size="small" @click="reset2()">重置</el-button>
        </div>
        <br />

        <elx-editable
            ref="elxEditable"
            class="table"
            size="mini"
            border
            :data.sync="list"
            :edit-config="{ trigger: 'click', mode: 'cell', activeMethod }"
            style="width: 100%"
        >
            <elx-editable-column type="index" width="55"></elx-editable-column>
            <elx-editable-column prop="id" label="账户号" ></elx-editable-column>
            <elx-editable-column prop="bank" label="开户支行" ></elx-editable-column>
            <elx-editable-column prop="money" label="余额" :edit-render="{ type: 'default' }"></elx-editable-column>
            <elx-editable-column prop="open_date" label="开户日期"></elx-editable-column>
            <elx-editable-column prop="type" label="账户类型" :edit-render="{ name: 'ElSelect', options: typeList }"></elx-editable-column>
            <elx-editable-column prop="interest" label="利率" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
            <elx-editable-column prop="cashtype" label="货币类型" :edit-render="{ name: 'ElSelect', options: cashList }"></elx-editable-column>
            <elx-editable-column prop="overdraft" label="透支额" :edit-render="{ name: 'ElInputNumber' }"></elx-editable-column>
            <elx-editable-column label="操作" width="350">
                <template v-slot="scope">
                    <el-button size="small" type="primary" @click="saveRowEvent(scope.row)">提交</el-button>
                    <el-button size="small" type="danger" @click="removeEvent(scope.row)">销户</el-button>
                    <el-button size="small" type="success" @click="showDetail(scope.row)">查看户主</el-button>
                </template>
            </elx-editable-column>
        </elx-editable>
        <div v-if="showlink">
            <p style="color: red;font-size: 24px;" align="left">
                户主信息表
                <el-button type="success" size="small" @click="showlink = false">关闭</el-button>
            </p>
            <div align="left">
                新增户主
                <input
                    type="text"
                    min="0"
                    placeholder="身份证号"
                    id="newOwner"
                    v-model="newOwner"
                    required="false"
                    style=" width:250px;font-family: 'Fira Code', '汉仪南宫体简';"
                />
                <el-button type="success" size="small" @click="addOwner()">提交</el-button>
            </div>
            <br>
            <elx-editable
                ref="elxEditable2"
                class="table"
                border
                :data.sync="ownerlist"
                :edit-config="{ trigger: 'manual', mode: 'row', clearActiveMethod: clearActiveMethod2 }"
                style="width: 100%"
            >
                <elx-editable-column type="index" width="55"></elx-editable-column>
                <elx-editable-column prop="id" label="账户号"></elx-editable-column>
                <elx-editable-column prop="bank" label="开户银行"></elx-editable-column>
                <elx-editable-column prop="ownerid" label="户主身份证号"></elx-editable-column>
                <elx-editable-column prop="ownername" label="户主姓名"></elx-editable-column>
                <elx-editable-column
                    prop="visit_date"
                    label="最近访问日期"
                    :edit-render="{
                        name: 'ElDatePicker',
                        props: { type: 'date', format: 'yyyy-MM-dd' }
                    }"
                ></elx-editable-column>
                <elx-editable-column label="操作" width="160">
                    <template v-slot="scope">
                        <el-button size="small" type="danger" @click="removeOwner(scope.row)">删除</el-button>
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
            newbankname: "",
            newmoneytype: "0",
            newbankid: "",
            newtype: "0",
            showlink: false,
            newOwner: "",
            detail: "",
            ownerlist: [],
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
            permission: "",
            newownerid: "",
            primary: null //全局变量，保存记录修改前的主键。当没有活跃的记录时为null，当新增记录时也为null
        };
    },
    created() {
        this.permission = localStorage.getItem("type");
        if (this.permission != "EMPLOYEE" && this.permission != "SUB_BANK" && this.permission != "CUSTOMER") {
            this.$router.push("/404");
        }
        this.findList();
        this.typeSearch = "any";
    },
    methods: {
        findList() {
            this.loading = true;
            this.list = [
                // {
                //     id: "123000",
                //     owner: "张三，李四，王五，马云，刘强东",
                //     bank: "合肥支行",
                //     money: 2563.0,
                //     open_date: new Date("2016-2-20"),
                //     visit_date: new Date(),
                //     type: "0",
                //     interest: 0.023,
                //     cashtype: "0",
                //     overdraft: null
                // }
            ];
            this.loading = false;
        },
        activeMethod({ row, column }) {
            if (column.label == "账户号" || column.label == "开户支行" || column.label == "账户类型" || column.label == "货币类型") {
                return false;
            }
            if (row.type == "0" && column.label == "透支额") {
                return false;
            }
            if (row.type == "1" && column.label == "利率") {
                return false;
            }
            return true;
        },
        clearActiveMethod2({ type, row, rowIndex }) {
            return false;
        },
        formatterDate(row, column, cellValue, index) {
            return XEUtils.toDateString(cellValue, "yyyy-MM-dd");
        },
        //开户
        newaccount() {
            if (this.newbankid == "" || this.newbankname == "" || this.newownerid == "") {
                return;
            }
            this.$http
                .post(
                    "http://" + document.domain + ":5000/account",
                    {
                        type: "Update",
                        id: this.newbankid,
                        bank: this.newbankname,
                        money: 0,
                        ownerid: this.newownerid,
                        open_date: XEUtils.toDateString(new Date(), "yyyy-MM-dd"),
                        acctype: this.newtype,
                        interest: null,
                        cashtype: this.newmoneytype,
                        overdraft: null,
                        old_primary: null
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        //更新合法
                        this.$refs.elxEditable.insert({
                            id: this.newbankid,
                            bank: this.newbankname,
                            money: 0,
                            open_date: XEUtils.toDateString(new Date(), "yyyy-MM-dd"),
                            type: this.newtype,
                            interest: null,
                            cashtype: this.newmoneytype,
                            overdraft: null
                        });
                        Message({message:"开户成功",type:"success"});
                    } else {
                        Message({message:"开户失败，您提供的信息可能有误或您已经在该支行开设同类账户",type:"warning"});
                    }
                });
        },

        insertEvent() {
            console.log("insert");
            let activeInfo = this.$refs.elxEditable.getActiveRow();
            //let { insertRecords } = this.$refs.elxEditable.getAllRecords();
            console.log(activeInfo);
            //console.log(insertRecords);
            if (!activeInfo) {
                this.$refs.elxEditable
                    .insert({
                        id: "new id",
                        owner: "",
                        bank: "",
                        money: 0,
                        open_date: XEUtils.toDateString(new Date(), "yyyy-MM-dd"),
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
            this.isClearActiveFlag = false;
            MessageBox.confirm("该数据未保存，是否移除?", "温馨提示", {
                distinguishCancelAndClose: true,
                confirmButtonText: "放弃修改",
                cancelButtonText: "返回继续",
                type: "warning"
            })
                .then(action => {
                    if (action === "confirm") {
                        this.$refs.elxEditable.clearActive();
                        this.$refs.elxEditable.revert(row);
                        if (this.primary == null) {
                            this.$refs.elxEditable.remove(row);
                        }
                        this.primary = null;
                    }
                })
                .catch(action => action)
                .then(() => {
                    this.isClearActiveFlag = true;
                });
        },
        //删除某一行
        removeEvent(row) {
            this.$http
                .post(
                    "http://" + document.domain + ":5000/account",
                    {
                        type: "Delete",
                        primary: row.id,
                        acctype: row.type
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.$refs.elxEditable.remove(row);
                        Message({message:"删除成功",type:"success"});
                    } else {
                        Message({message:"删除失败",type:"warning"});
                    }
                });
        },
        //保存对某一行的修改
        saveRowEvent(row) {
            if (this.$refs.elxEditable.hasRowChange(row)) {
                //数据发生了修改，需要反馈给服务器
                this.$http
                    .post(
                        "http://" + document.domain + ":5000/account",
                        {
                            type: "Update",
                            id: row.id,
                            bank: row.bank,
                            money: row.money,
                            ownerid: null,
                            open_date: row.open_date,
                            acctype: row.type,
                            interest: row.interest,
                            cashtype: row.cashtype,
                            overdraft: row.overdraft,
                            old_primary: row.id //null代表新增
                        },
                        {
                            emulateJSON: true
                        }
                    )
                    .then(function(response) {
                        if (parseInt(response.body.code) === 200) {
                            //更新合法
                            this.$refs.elxEditable.clearActive();
                            this.$refs.elxEditable.reloadRow(row);
                            Message({message:"保存成功",type:"success"});
                        } else {
                            Message({message:"保存失败，可能是账户号已存在",type:"warning"});
                        }
                    });
            }
        },
        //导出CSV
        exportCsvEvent() {
            this.$refs.elxEditable.exportCsv();
        },
        //提交查询请求
        submit() {
            this.showlink=false;
            this.$http
                .post(
                    "http://" + document.domain + ":5000/account",
                    {
                        type: "Search",
                        bankSearch: this.bankSearch,
                        idSearch: this.idSearch,
                        ownerSearch: this.ownerSearch,
                        typeSearch: this.typeSearch,
                        money_lo: this.money_lo,
                        money_up: this.money_up,
                        open_lo: XEUtils.toDateString(this.open_lo, "yyyy-MM-dd"),
                        open_up: XEUtils.toDateString(this.open_up, "yyyy-MM-dd"),
                        visit_lo: XEUtils.toDateString(this.visit_lo, "yyyy-MM-dd"),
                        visit_up: XEUtils.toDateString(this.visit_up, "yyyy-MM-dd")
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.list = response.body.list;
                        Message({message:"查询成功",type:"success"});
                    } else {
                        Message({message:"查询结果为空",type:"warning"});
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

        addOwner() {
            if (this.newOwner == "") {
                return;
            }
            this.$http
                .post(
                    "http://" + document.domain + ":5000/accountCustomer",
                    {
                        type: "Insert",
                        accid: this.detail.id,
                        bank: this.detail.bank,
                        visit_date: XEUtils.toDateString(new Date(), "yyyy-MM-dd"),
                        ownerid: this.newOwner,
                        acctype: this.detail.type
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.ownerlist.push(response.body.record);
                        Message({message:"新增户主成功",type:"success"});
                    } else {
                        Message({message:"新增户主失败，可能是身份证号错误或其已经在该支行开设同类账户",type:"warning"});
                    }
                });
        },
        removeOwner(row) {
            this.$http
                .post(
                    "http://" + document.domain + ":5000/accountCustomer",
                    {
                        type: "Delete",
                        accid: this.detail.id,
                        bank: this.detail.bank,
                        ownerid: row.ownerid,
                        acctype: this.detail.type
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.$refs.elxEditable2.remove(row);
                        Message({message:"删除成功",type:"success"});
                    } else {
                        window.alert("删除失败");
                    }
                });
        },
        searchOwner(row) {
            this.$http
                .post(
                    "http://" + document.domain + ":5000/accountCustomer",
                    {
                        type: "Search",
                        accid: this.detail.id,
                        bank: row.bank,
                        acctype: row.type
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.ownerlist = response.body.list;
                        for (var i = 0; i < this.ownerlist.length; i++) {
                            this.ownerlist[i].id = row.id;
                            this.ownerlist[i].bank = row.bank;
                        }
                        Message({message:"查询成功",type:"success"});
                    } else {
                        this.ownerlist=[];
                        Message({message:"查询失败",type:"error"});
                    }
                });
        },
        showDetail(row) {
            this.showlink = true;
            this.detail = row;
            console.log("update");
            console.log(row.id);
            this.searchOwner(row);
        },
        reset2() {
            this.newbankname = "";
            this.newmoneytype = "0";
            this.newbankid = "";
            this.newtype = "0";
            this.newownerid = "";
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
    width: 100px;
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
