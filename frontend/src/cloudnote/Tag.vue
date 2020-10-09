<template>
  <div>
  <el-tag
  :key="tag"
  v-for="tag in dynamicTags"
  closable
  :disable-transitions="false"
  @close="handleClose(tag)" >
  {{tag}}
</el-tag>
<el-input
class="input-new-tag"
v-if="inputVisible"
v-model="inputValue"
ref="saveTagInput"

@keyup.enter.native="handleInputConfirm"
@blur="handleInputConfirm"
>
</el-input>
<el-button v-else class="button-new-tag"  @click="showInput">+ 添加标签</el-button>
</div>
</template>

<style>
.el-tag {
  margin-left: 25px;
  margin-bottom: 2px;
  margin-top: 2px;
}
.button-new-tag {
  margin-left: 10px;
  margin-top: 4px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>

<script>
export default {
  name:"Tag",
  data() {
    return {
      dynamicTags: [],
      inputVisible: false,
      inputValue: ''
    };
  },
  methods: {
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
    },

    showInput() {
      this.inputVisible = true;
      this.$nextTick(() => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },

    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.dynamicTags.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = '';
    }
  }
}
</script>