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
            <button class="button" v-on:click="start()">
                <span>提交</span>
            </button>
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
                    }
                });
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
    border-collapse: collapse; /* 边框重叠 */
    overflow-x: auto;
    overflow-y: auto;
    white-space: nowrap;
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
    min-width: 100px;
    text-align: center;
}
.table td {
    border: 1px solid #429fff; /* 单元格边框 */
    text-align: center;
    padding: 4px;
    min-width: 100px;
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
