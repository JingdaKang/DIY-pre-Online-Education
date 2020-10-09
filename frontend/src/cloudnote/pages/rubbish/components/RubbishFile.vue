<template>
    <div style="padding-left: 1%;">
        <el-row>
            <el-col :span="16" >
                <el-tooltip  effect="light"  placement="right">
                    <div slot="content">
                        <el-link icon="el-icon-refresh-right" @click="Recover"></el-link>
                        <el-divider direction="vertical"></el-divider>
                        <el-link icon="el-icon-delete" @click="DeleteForever"> </el-link>


                    </div>
                    <el-link style="font-weight: bolder;font-size: 17px" @click="dialogVisible=true" target="_blank"  >
                        <i class="el-icon-document" style="margin-right: 1px"></i>
                    {{FileInfo.note_title}}</el-link>

                </el-tooltip>
            </el-col>
            <!--                    日期-->
            <el-col  :span="4" style="float: right;margin-right: 5%">

                <i class="el-icon-date" style="color: #409EFF">{{FileInfo.note_delete}}</i>


            </el-col>
        </el-row>
        <!--                横线-->
        <el-row>
            <hr  >
        </el-row>

        <el-dialog
                title="内容"
                :visible.sync="dialogVisible"
                width="90%"

        >
    <div style="">
        <makedown-show
        background="#6062665e"
        :mk-value="mkValue" ></makedown-show>
    </div>

        </el-dialog>
    </div>
</template>

<script>

import MakedownShow from "@/cloudnote/makedownShow";

export default {
    name: "RublishFile",
    props:["FileInfo"],
    data:function () {
        return {
            dialogVisible:false
        }
    },
    methods:{
        Recover(){
            this.$emit("Recover",this.FileInfo.id)
        },
        DeleteForever(){
            this.$emit("DeleteForever",this.FileInfo.id)
        }
    },
    computed:{
        mkValue(){
            return this.FileInfo.note_text;
        }
    },
    components: {MakedownShow},
}
</script>

<style scoped>

</style>
