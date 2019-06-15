<template>
    <div v-loading="loading">
        <h1>业务统计</h1>
        <p style="color: red;font-size: 24px;" align="left">统计条件</p>
        <form align="left" onSubmit="return false">
            时间范围
            <input
                type="month"
                min="0"
                placeholder="开始时间"
                id="lowerBound"
                v-model="lowerBound"
                required="true"
                style=" width:200px;
                font-family: 'Fira Code', '汉仪南宫体简';
                "
            />~~
            <input
                type="month"
                min="0"
                placeholder="停止时间"
                id="upperBound"
                v-model="upperBound"
                required="true"
                style=" width:200px;
                font-family: 'Fira Code', '汉仪南宫体简';
                "
            />&emsp;时间粒度
            <select v-model="timegrain" id="timegrain" placeholder="month">
                <option value="month" selected>月</option>
                <option value="season">季</option>
                <option value="year">年</option> </select
            >&emsp;业务分类
            <select v-model="sumtype" id="sumtype" placeholder="all">
                <option value="all" selected>所有</option>
                <option value="saving">储蓄业务</option>
                <option value="loan">贷款业务</option> </select
            >&emsp;统计项目
            <select v-model="datatype" id="datatype" placeholder="all">
                <option value="money">业务总金额</option>
                <option value="user">用户数</option> </select
            >&emsp;
            <input
                type="radio"
                name="graphtype"
                v-model="graphtype"
                value="curve"
                required="true"
            />按时间统计&emsp;
            <input
                type="radio"
                name="graphtype"
                v-model="graphtype"
                value="pie"
                required="true"
            />按支行统计&emsp;
            <el-button type="primary" v-on:click="start()">
                <span>提交</span>
            </el-button>
        </form>
        <template v-if="result">
            <p style="color: red;font-size: 24px;" align="left">统计表</p>
            <div>
                <elx-editable
                    ref="elxEditable1"
                    size="small"
                    class="table"
                    border
                    :data.sync="userList"
                    :edit-config="{ trigger: 'manual', mode: 'row' }"
                    style="width: 100%"
                >
                    <elx-editable-column
                        prop="time"
                        label="时间"
                        :edit-render="{ name: 'ElInput' }"
                    ></elx-editable-column>
                    <template v-for="item in columnConfigs">
                        <template v-if="item._show">
                            <elx-editable-column
                                v-bind="item"
                                :key="item.prop"
                            ></elx-editable-column>
                        </template>
                    </template>
                </elx-editable>
            </div>
            <p style="color: red;font-size: 24px;" align="left">统计图</p>
            <img src="static/summary.png" alt="业务统计图" width="100%" />
        </template>
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
            result: false,
            isClearActiveFlag: true,
            columnConfigs: [
                {
                    prop: "bank1",
                    label: "合肥支行",
                    _show: true
                },
                {
                    prop: "bank2",
                    label: "南京支行",
                    _show: true
                },
                {
                    prop: "bank3",
                    label: "北京支行",
                    _show: true
                }
            ],
            userList: [
                {
                    time: "2016年",
                    bank1: "12",
                    bank2: "13",
                    bank3: "1332"
                },
                {
                    time: "2017年",
                    bank1: "12",
                    bank2: "13",
                    bank3: "1332"
                },
                {
                    time: "2018年",
                    bank1: "12",
                    bank2: "13",
                    bank3: "1332"
                }
            ],
            upperBound: "",
            lowerBound: "",
            timegrain: "",
            sumtype: "",
            datatype: "",
            graphtype: "",
            permission: ""
        };
    },
    created() {
        this.permission = localStorage.getItem("type");
        if (this.permission != 'SUB_BANK') {
            this.$router.push("/404");
        }
        this.timegrain = "month";
        this.sumtype = "all";
        this.datatype = "money";
        this.graphtype = "curve";
    },
    methods: {
        start: function() {
            if (this.upperBound == "" || this.lowerBound == "") {
                Message({message:"时间范围不能为空",type:"warning"});
                return;
            }
            this.$http
                .post(
                    "http://" + document.domain + ":5000/summary",
                    {
                        upperBound: XEUtils.toDateString(this.upperBound, "yyyy-MM-dd"),
                        lowerBound: XEUtils.toDateString(this.lowerBound, "yyyy-MM-dd"),
                        timegrain: this.timegrain,
                        sumtype: this.sumtype,
                        datatype: this.datatype,
                        graphtype: this.graphtype
                    },
                    {
                        emulateJSON: true
                    }
                )
                .then(function(response) {
                    if (parseInt(response.body.code) === 200) {
                        this.columnConfigs = [];
                        this.result = true;
                        let tempList = response.body.columnList;
                        tempList.forEach(column => {
                            let item = {
                                prop: column,
                                label: column,
                                _show: true
                            };
                            this.columnConfigs.push(item);
                        });
                        this.userList = response.body.rawData;
                        Message({message:"查询成功",type:"success"});
                    }
                });
        }
    }
};
</script>

<style>
</style>
