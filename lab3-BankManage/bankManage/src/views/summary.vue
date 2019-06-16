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
                class="input"
                id="lowerBound"
                v-model="lowerBound"
                required="true"
                style=" width:180px;
                font-family: 'Fira Code', '汉仪南宫体简';
                "
            />~~
            <input
                type="month"
                min="0"
                placeholder="停止时间"
                class="input"
                id="upperBound"
                v-model="upperBound"
                required="true"
                style=" width:180px;
                font-family: 'Fira Code', '汉仪南宫体简';
                "
            />&emsp;时间粒度
            <select class="dropbtn" v-model="timegrain" id="timegrain" placeholder="month">
                <option value="month" selected>月</option>
                <option value="season">季</option>
                <option value="year">年</option> </select
            >&emsp;业务分类
            <select class="dropbtn" v-model="sumtype" id="sumtype" placeholder="all">
                <!-- <option value="all" selected>所有</option> -->
                <option value="saving" selected>储蓄业务</option>
                <option value="loan">贷款业务</option> </select
            >&emsp;统计项目
            <select class="dropbtn" v-model="datatype" id="datatype" placeholder="all">
                <option value="money" selected>业务总金额</option>
                <option value="user">用户数</option> </select
            >&emsp;
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
                    <elx-editable-column prop="time" label="时间"></elx-editable-column>
                    <template v-for="item in columnConfigs">
                        <template v-if="item._show">
                            <elx-editable-column v-bind="item" :key="item.prop"></elx-editable-column>
                        </template>
                    </template>
                </elx-editable>
            </div>
            <p style="color: red;font-size: 24px;" align="left">统计图</p>
            <div align="left">
                <div class="radio">
                <input id="radio-1" type="radio" name="graphtype" v-model="graphtype" value="curve" required="true" />
                <label for="radio-1" class="radio-label">按时间统计</label>&emsp;
                <input id="radio-2" type="radio" name="graphtype" v-model="graphtype" value="pie" required="true" />
                <label for="radio-2" class="radio-label">按支行统计</label>&emsp;
                </div>
            </div>
            <div align="center">
                <ve-pie :data="chartData" v-if="graphtype=='pie'" width="800px"></ve-pie>
                <ve-line :data="chartData2" :settings="chartSettings" width="800px" v-else></ve-line>
            </div>
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
            showpie: false,
            chartSettings: {},
            list: [],
            result: false,
            isClearActiveFlag: true,
            chartData: {},
            chartData2: {},
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
            upperBound: "2019-06",
            lowerBound: "2015-01",
            timegrain: "",
            sumtype: "",
            datatype: "",
            graphtype: "",
            permission: ""
        };
    },
    created() {
        this.permission = localStorage.getItem("type");
        if (this.permission != "SUB_BANK") {
            this.$router.push("/404");
        }
        this.timegrain = "month";
        this.sumtype = "saving";
        this.datatype = "money";
        this.graphtype = "curve";
    },
    methods: {
        start: function() {
            if (this.upperBound == "" || this.lowerBound == "") {
                Message({ message: "时间范围不能为空", type: "warning" });
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
                        graphtype: "curve"
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
                        this.cleanData(response.body.columnList, response.body.rawData);
                        this.makePieChart(response.body.columnList, response.body.rawData);
                        this.makeLineChart(response.body.columnList, response.body.rawData);
                        Message({ message: "查询成功", type: "success" });
                    }else {
                        this.result=false;
                        Message({ message: "查询结果为空", type: "warning" });
                    }
                });
        },
        cleanData: function(columnList, rawData){
            //console.log();
            for (var i = 0; i < rawData.length; i++) {
                for (var j = 0; j < columnList.length; j++) {
                    if (rawData[i][columnList[j]]==null){
                        rawData[i][columnList[j]]=0;
                    }
                }
            }
            for (var i=0;i<rawData.length;i++){
                if (rawData[i].time.indexOf('.')!=-1){                    
                    XEUtils.toStringDate(rawData[i], 'yyyy.mm');
                }
            }
            for (var i=0;i<rawData.length;i++){
                for (var j=i+1;j<rawData.length;j++){
                    if (rawData[i].time>rawData[j].time){
                        var temp=rawData[i];
                        rawData[i]=rawData[j];
                        rawData[j]=temp;
                    }
                }
            }
        },
        makePieChart: function(columnList, rawData) {
            //只有当用户选择按支行统计时，才会制作饼图，将同一支行在所有时间的值都加起来，显示在饼图上
            //饼图有两个维度，一个是支行名，一个是要统计的指标
            //var index=(this.datatype==='money')? '业务总金额':'用户数';
            this.chartData.columns = [];
            this.chartData.rows = []; //清空图片数据
            this.chartData.columns = ["支行", "index"];
            for (var i = 0; i < columnList.length; i++) {
                this.chartData.rows.push({ 支行: columnList[i], index: 0 });
            }
            for (var i = 0; i < rawData.length; i++) {
                for (var j = 0; j < columnList.length; j++) {
                    this.chartData.rows[j].index += rawData[i][columnList[j]];
                }
            }
        },
        makeLineChart: function(columnList, rawData) {
            this.chartData2.columns = [];
            this.chartData2.columns.push("time");
            for (var i = 0; i < columnList.length; i++) {
                this.chartData2.columns.push(columnList[i]);
            }
            this.chartData2.rows = rawData;
            this.chartSettings = {
                metrics: columnList,
                dimension: ["time"],
                min: ["dataMin", "dataMin"],
                max: ["dataMax", "dataMax"]
            };
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
    width: 150px;
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
.radio {
    margin: 0.5rem;
}
.radio input[type="radio"] {
    position: absolute;
    opacity: 0;
}
.radio input[type="radio"] + .radio-label:before {
    content: '';
    background: #f4f4f4;
    border-radius: 100%;
    border: 1px solid #b4b4b4;
    display: inline-block;
    width: 1.2em;
    height: 1.2em;
    position: relative;
    top: -0.2em;
    margin-right: 0.3em;
    vertical-align: top;
    cursor: pointer;
    text-align: center;
    -webkit-transition: all 250ms ease;
    transition: all 250ms ease;
}
.radio input[type="radio"]:checked + .radio-label:before {
    background-color: #3197EE;
    box-shadow: inset 0 0 0 4px #f4f4f4;
}
.radio input[type="radio"]:focus + .radio-label:before {
    outline: none;
    border-color: #3197EE;
}
.radio input[type="radio"]:disabled + .radio-label:before {
    box-shadow: inset 0 0 0 4px #f4f4f4;
    border-color: #b4b4b4;
    background: #b4b4b4;
}
.radio input[type="radio"] + .radio-label:empty:before {
    margin-right: 0;
}
</style>
