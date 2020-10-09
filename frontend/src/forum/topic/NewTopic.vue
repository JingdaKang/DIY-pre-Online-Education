<template>
  <div class="page-container">
    <div class="main">
      <h1 class="el-icon-albb-brush">创作主题</h1>
      <div class="write-topic">
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
            <div class="config">
              <span>请选择板块：</span>
              <el-select v-model="form.tags" size="small" placeholder="发布板块" style="margin-right: 10px;" clearable>
                <el-option
                  v-for="item in sectionData"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </div>
          </el-form-item>

          <el-form-item prop="file">
            <span>上传文件(可选):</span>
            <input type="file" id="upload"/>

          </el-form-item>

          <el-form-item>
            <el-button  type="primary" @click="submit()">提交</el-button>
          </el-form-item>
        </el-form>

      </div>
    </div>
  </div>
</template>

<script>
  import {mavonEditor} from 'mavon-editor'
  export default {
      name: "NewTopic",
      components: {
        mavonEditor
      },

      created () {
        this.getTags()
      },
      data () {
        return {
          user: window.localStorage.getItem('username'),
          sectionData: [],
          form: {
            title: '',
            tags: '',
            content: '',
            file: ''
          },
          rules: {
            title: [{required: true, message: '这是必填的!', trigger: 'blur'}],
            content: [{required: true, message: '这是必填的!', trigger: 'blur'}],
            tags: [{required: true, message: '这是必填的!', trigger: 'blur'}],
          }
        }
      },
      methods: {
        getTags () {
          this.axios.get("/forum/sections/", {
          }).then(response => {
            if (response.data.status === 0) {
              this.sectionData = response.data.data
            }
          })
        },
        submit () {
          const topicData = this.form
          var data = new FormData();
          var uploadFile = document.getElementById('upload').files[0];
          console.log(uploadFile)
          if(typeof(uploadFile)!="undefined"){
            data.append('file', uploadFile, uploadFile.name)
            console.log("upload success")

          }
          data.append('section_id', topicData.tags)
          data.append('topic_title', topicData.title)
          data.append('topic_content', topicData.content)
          let headers = {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
          this.axios.post('/forum/addTopic', data, headers)
            .then(response => {
            if (response.data.status === 0) {
              const newTopicId = response.data.topic_id
              this.$router.push({ path: `/forum/topic/${newTopicId}`})
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
