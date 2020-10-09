<template>
  <div class="page-container">
    <div class="main">
      <h1 class="el-icon-albb-brush">编辑</h1>
      <div class="write">
        <el-form ref="form" :model="form">
          <!-- 标题 -->
          <el-form-item>
            <div class="title">
              <el-input v-model="form.title" :autofocus="true" class="input-with-select" placeholder="标题" />
            </div>
          </el-form-item>

          <br>

          <el-form-item>
            <!-- 内容 -->
            <mavon-editor class="mavon-editor" v-model="form.content" :max-height="'100%'" />
            <br>
          </el-form-item>

          <br>

          <el-form-item>
            <el-button type="primary" @click="submit()">提交</el-button>
          </el-form-item>
        </el-form>

      </div>
    </div>
  </div>
</template>

<script>
  import {mavonEditor} from 'mavon-editor'
  export default {
    name: "EditDiscuss",
    components: {
      mavonEditor
    },

    created () {
      this.init()
      this.getTopicDetail()
    },
    data () {
      return {
        user: window.localStorage.getItem('username'),
        form: {
          id: '',
          title: '',
          content: ''
        },
      }
    },
    methods: {
      init () {
        const thisForm = this.form
        thisForm.id = this.$route.params.id
      },
      getTopicDetail () {
        this.axios.get('/forum/discuss/' + this.$route.params.id + '/')
          .then(response => {
            if (response.data.status === 0) {
              this.form.title = response.data.data.discuss_title
              this.form.content = response.data.data.discuss_content

            }
          })
          .catch(err => {
            console.error("获取详情异常", err)
          });

      },
      submit () {
        const topicData = this.form
        var data = new FormData();
        data.append('discuss_id', topicData.id)
        data.append('discuss_title', topicData.title)
        data.append('discuss_content', topicData.content)
        let headers = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }


        this.axios.post('/forum/editGroupDiscuss', data, headers)
          .then(response => {
            if (response.data.status === 0) {
              const discuss_id = response.data.discuss_id
              this.$router.push({ path: `/forum/discuss/${discuss_id}`})
              this.$message({
                showClose: true,
                message: response.data.message,
                type: response.success === 0 ? 'success' : 'error',
                duration: 2000
              })
            } else {
              this.$message({
                showClose: true,
                message: response.data.message,
                type: response.success === 0 ? 'success' : 'error',
                duration: 2000
              })
            }
          })
      },
    }
  }

</script>

<style scoped lang="scss">
  .mavon-editor{
    height: 550px;
  }

</style>
