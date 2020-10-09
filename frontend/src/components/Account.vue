<template>
  <div id="Account">
    <el-row>
      <p style="font-size:20px;font-weight:bold;margin-top:25px">
        账户管理
      </p>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <el-form label-width="80px">
        <el-col :span="6">
          <el-form-item prop="name" label="账户名">
            <el-input v-model="name" style="float:left;width:90%;margin-left:10px"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item prop="type" label="账户类型">
            <el-select v-model="user_type" style="float: left;margin-left: 25px">
              <el-option label="不限" value=""></el-option>
              <el-option label="教师" value="T"></el-option>
              <el-option label="学生" value="S"></el-option>
              <el-option label="管理员" value="A"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item prop="status" label="账户状态">
            <el-select v-model="status" style="float: left;margin-left: 25px">
              <el-option label="不限" value=""></el-option>
              <el-option label="停用" value="1"></el-option>
              <el-option label="活跃" value="2"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" style="float:left;margin-left: 0px"
                       v-on:click="get_account_by_condition">查询
            </el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>
    <el-table :data="page_accounts" ref="account"
              style="width: 100%;margin-top:20px" border>
      <el-table-column prop="name" label="账户名" min-width="100" align="center">
        <template slot-scope="scope">
          {{scope.row.username}}
        </template>
      </el-table-column>
      <el-table-column prop="type" label="账户类型" min-width="100" align="center">
        <template slot-scope="scope">
          <p v-if="scope.row.type=='S'">学生</p>
          <p v-if="scope.row.type=='T'">教师</p>
          <p v-if="scope.row.type=='A'">管理员</p>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="账户状态" min-width="100" align="center">
        <template slot-scope="scope">
          <el-row>
            <button v-if="scope.row.is_active==true" type="button"
                    class="el-button el-button--mini el-button--success is-circle"><i
              class="el-icon-check"></i>
            </button>
            <button v-if="scope.row.is_active==false" type="button"
                    class="el-button el-button--mini el-button--info is-circle"><i
              class="el-icon-close"></i>
            </button>
          </el-row>
        </template>
      </el-table-column>
      <el-table-column prop="option" label="操作" min-width="100" align="center">
        <template slot-scope="scope">
          <el-row>
            <p v-if="scope.row.is_active==true">停用</p>
            <p v-if="scope.row.is_active==false">启用</p>
            <el-switch
              v-model="scope.row.is_active"
              active-color="#13ce66"
              inactive-color="#ff4949"
            @change="change_status(scope.row.id)">
            </el-switch>
          </el-row>
        </template>
      </el-table-column>
    </el-table>
    <el-row style="margin-top:20px">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 6, 8, 10]"
        :page-size="5"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalCount">
      </el-pagination>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "Account",
    data() {
      return {
        name: '',
        user_type: '',
        status: '',
        loading: false,
        currentPage: 1,
        totalCount: '',
        pageSize: 5,
        accountList: [],
        page_accounts: []
      }
    },
    mounted() {
      this.get_accounts()
    },
    methods: {
      get_account_by_condition() {
        let that = this
        let name = that.name
        let type = that.user_type
        let status = that.status
        let param = new URLSearchParams()
        param.append('name', name)
        if (type.length > 0) {
          param.append('type', type)
        } else {
          param.append('type', 0)
        }
        if (status == '1') {
          param.append('status', 'False')
        } else if (status == '2') {
          param.append('status', 'True')
        } else {
          param.append('status', 0)
        }
        that.axios({
          method: 'post',
          url: '/api/get_account_by_condition/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.accountList = res.data.condition_accounts
              that.totalCount = that.accountList.length
              that.get_page_account()
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_accounts() {
        let that = this
        that.axios.get('/api/accounts/')
          .then(function (res) {
            if (res.data.code === 1) {
              that.accountList = res.data.accounts
              that.totalCount = that.accountList.length
              console.log(that.accountList)
              that.get_page_account()
              console.log(that.page_accounts)
            } else if (res.data.code === 0) {
              that.$message.error('查询失败')
            }
          })
      },
      get_page_account() {
        this.page_accounts = [];
        for (let i = (this.currentPage - 1) * this.pageSize; i < this.totalCount; i++) {
          this.page_accounts.push(this.accountList[i])
          if (this.page_accounts.length == this.pageSize) break;
        }
      },
      handleSizeChange(val) {
        this.pageSize = val;
        this.get_page_account()
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        this.get_page_account()
      },
      change_status(value) {
        let that = this
        let param = new URLSearchParams()
        param.append('id', value)
        that.axios({
          method: 'post',
          url: '/api/change_status/',
          data: param
        })
          .then(function (res) {
            if (res.data.code === 1) {
              that.$message.success('修改成功')
            } else if (res.data.code === 0) {
              that.$message.error('修改失败')
            }
          })
      }
    }
  }
</script>

<style scoped>

</style>
