<template>
    <div  style="padding-top: 1%;">

        <el-row>
            <el-col :span="19">
                <span style="font-weight: bold;font-size:20px">回收站</span>



            </el-col>

            <el-col :span="5">
                <el-button type="primary" style="float: right" round size="mini" @click="ForeverDelete"><i class="el-icon-check" style="margin-right: 4px"></i>清空回收站</el-button>

            </el-col>



        </el-row>
    </div>
</template>

<script>
export default {
    name: "TopBar",
    methods:{
        ForeverDelete(){
            this.$emit("ForeverDelete");
        }
    }
}
</script>

<style scoped>

</style>