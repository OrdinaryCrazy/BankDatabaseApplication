<template>
  <div v-loading="loading">
    <h1>支行管理</h1>
    <p style="color: red;font-size: 24px;" align="left">条件筛选</p>
    <div align="left">
    支行名称
    <input 
      type="text" 
      placeholder="包含关键字" 
      id="bankSearch"
      v-model="bankSearch"
      required=false
      style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
    >&emsp;所在城市
    <input 
      type="text" 
      placeholder="包含关键字" 
      id="citySearch"
      v-model="citySearch"
      required=false
      style=" width:300px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
    >&emsp;资产总额
    <input 
      type="number" 
      placeholder="下界" 
      id="lowerBound"
      v-model="lowerBound"
      required=false
      style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
    >~~
    <input 
      type="number" 
      placeholder="上界" 
      id="upperBound"
      v-model="upperBound"
      required=false
      style=" width:100px;
              font-family: 'Fira Code', '汉仪南宫体简';
            "
    >&emsp;
    <el-button class="button" size="small" type="primary" @click="submit()">查询</el-button>
    <el-button class="button" size="small" type="primary" @click="reset()">重置</el-button>

    </div><br>
    <div align="left" >
      <el-button class="button" type="success" size="small" @click="insertEvent">新增</el-button>
      <el-button class="button" type="success" size="small" @click="exportCsvEvent">导出</el-button>
    </div>
    <br><br>
    <elx-editable
      ref="elxEditable"
      class="table"
      border
      :data.sync="list"
      :edit-config="{trigger: 'manual', mode: 'row', clearActiveMethod}"
      style="width: 100%">
      <elx-editable-column
        type="index"
        width="55"></elx-editable-column>
      <elx-editable-column
        prop="name"
        label="支行名称"
        :edit-render="{name: 'ElInput'}"></elx-editable-column>
      <elx-editable-column
        prop="city"
        label="所在城市"
        :edit-render="{name: 'ElInput'}"></elx-editable-column>
      <elx-editable-column
        prop="money"
        label="资产总额"
        :edit-render="{name: 'ElInputNumber'}"></elx-editable-column>
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
  </div>
</template>

<script>
import XEUtils from 'xe-utils'
import XEAjax from 'xe-ajax'
import { MessageBox, Message } from 'element-ui'
export default {
  data () {
    return {
      loading: false,
      list: [],
      isClearActiveFlag: true,
      bankSearch: "",
      citySearch: "",
      lowerBound: "",
      upperBound: ""
    }
  },
  created () {
    this.findList()
  },
  methods: {
    findList () {
      this.loading = true;
      this.list=[
        {
            name: '合肥城南支行',
            city: '合肥',
            money: 100000000
        },
        {
            name: '合肥城东支行',
            city: '合肥',
            money: 25000000
        }
      ];
      this.loading = false

    },
    formatterDate (row, column, cellValue, index) {
      return XEUtils.toDateString(cellValue, 'yyyy-MM-dd HH:mm:ss')
    },
    clearActiveMethod ({ type, row }) {
      return this.isClearActiveFlag && type === 'out' ? this.checkOutSave(row) : this.isClearActiveFlag
    },
    insertEvent () {
      let activeInfo = this.$refs.elxEditable.getActiveRow()
      let { insertRecords } = this.$refs.elxEditable.getAllRecords()
      if (!activeInfo && !insertRecords.length) {
        this.$refs.elxEditable.insert({
          name: `New ${Date.now()}`,
          age: 26,
          flag: false
        }).then(({ row }) => {
          this.$refs.elxEditable.setActiveRow(row)
        })
      }
    },
    // 点击表格外面处理
    checkOutSave (row) {
      if (!row.id) {
        this.isClearActiveFlag = false
        MessageBox.confirm('该数据未保存，请确认操作?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '保存数据',
          cancelButtonText: '移除数据',
          type: 'warning'
        }).then(action => {
          this.$refs.elxEditable.clearActive()
          this.saveRowEvent(row)
        }).catch(action => {
          if (action === 'cancel') {
            this.$refs.elxEditable.remove(row)
          }
        }).then(() => {
          this.isClearActiveFlag = true
        })
      } else if (this.$refs.elxEditable.hasRowChange(row)) {
        this.isClearActiveFlag = false
        MessageBox.confirm('检测到未保存的内容，请确认操作?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '保存数据',
          cancelButtonText: '取消修改',
          type: 'warning'
        }).then(() => {
          this.$refs.elxEditable.clearActive()
          this.saveRowEvent(row)
        }).catch(action => {
          if (action === 'cancel') {
            this.$refs.elxEditable.revert(row)
            this.$refs.elxEditable.clearActive()
          }
        }).then(() => {
          this.isClearActiveFlag = true
        })
        return false
      }
      return this.isClearActiveFlag
    },
    // 编辑处理
    openActiveRowEvent (row) {
      this.$nextTick(() => {
        let activeInfo = this.$refs.elxEditable.getActiveRow()
        if (activeInfo && activeInfo.isUpdate) {
          this.isClearActiveFlag = false
          MessageBox.confirm('检测到未保存的内容，请确认操作?', '温馨提示', {
            distinguishCancelAndClose: true,
            confirmButtonText: '保存数据',
            cancelButtonText: '取消修改',
            type: 'warning'
          }).then(() => {
            this.$refs.elxEditable.setActiveRow(row)
            this.saveRowEvent(activeInfo.row)
          }).catch(action => {
            if (action === 'cancel') {
              this.$refs.elxEditable.revert(activeInfo.row)
              this.$refs.elxEditable.setActiveRow(row)
            }
          }).then(() => {
            this.isClearActiveFlag = true
          })
        } else {
          this.$refs.elxEditable.setActiveRow(row)
        }
      })
    },
    // 取消处理
    cancelRowEvent (row) {
      if (!row.id) {
        this.isClearActiveFlag = false
        MessageBox.confirm('该数据未保存，是否移除?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '移除数据',
          cancelButtonText: '返回继续',
          type: 'warning'
        }).then(action => {
          if (action === 'confirm') {
            this.$refs.elxEditable.remove(row)
          }
        }).catch(action => action).then(() => {
          this.isClearActiveFlag = true
        })
      } else if (this.$refs.elxEditable.hasRowChange(row)) {
        this.isClearActiveFlag = false
        MessageBox.confirm('检测到未保存的内容，是否取消修改?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '取消修改',
          cancelButtonText: '返回继续',
          type: 'warning'
        }).then(action => {
          this.$refs.elxEditable.clearActive()
          this.$refs.elxEditable.revert(row)
        }).catch(action => {
          if (action === 'cancel') {
            this.$refs.elxEditable.setActiveRow(row)
          }
        }).then(() => {
          this.isClearActiveFlag = true
        })
      } else {
        this.$refs.elxEditable.clearActive()
      }
    },
    removeEvent (row) {
      if (row.id) {
        this.isClearActiveFlag = false
        MessageBox.confirm('确定永久删除该数据?', '温馨提示', {
          distinguishCancelAndClose: true,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          XEAjax.doDelete(`/api/role/delete/${row.id}`).then(({ data }) => {
            this.findList()
          }).catch(e => {
            this.loading = false
          })
        }).catch(action => action).then(() => {
          this.isClearActiveFlag = true
        })
      } else {
        this.$refs.elxEditable.remove(row)
      }
    },
    saveRowEvent (row) {
      this.$refs.elxEditable.validateRow(row, valid => {
        if (valid) {
          let url = '/api/role/add'
          if (row.id) {
            url = '/api/role/update'
          }
          this.loading = true
          this.$refs.elxEditable.clearActive()
          XEAjax.doPost(url, row).then(({ data }) => {
            this.findList()
            Message({ message: '保存成功', type: 'success' })
          }).catch(e => {
            this.loading = false
          })
        }
      })
    },
    exportCsvEvent () {
      this.$refs.elxEditable.exportCsv()
    },
    submit(){

    },
    reset(){

    }
  }
}
</script>

<style>
.table {
    border: 2px solid #429fff; /* 表格边框 */
    font-family: '汉仪南宫体简';
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
}
.button {
  display: inline-block;
  border-radius: 4px;
  background-color: limegreen;
  border: none;
  color: #FFFFFF;
  text-align: center;
  font-size: 15px;
  padding: 5px;
  width: 80px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 5px;
}
</style>