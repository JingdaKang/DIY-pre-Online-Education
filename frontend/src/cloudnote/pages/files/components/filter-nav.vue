<template>
    <div>
        <el-row style="padding-top: 1%;padding-left:1%">

            <el-col :span="4">
                <el-input
                clearable
                placeholder="请输入内容"
                prefix-icon="el-icon-search"
                v-model="keywords"
                @change = "search"
                @clear = "clear">
            </el-input>
        </el-col>
        <el-col :span="10" style="padding-left: 4%">
            <el-radio-group v-model="filter"  size="medium" @change = "ascOrder">
                <el-radio-button label="时间升序" ></el-radio-button>

            </el-radio-group>
            <el-link :underline="false" type="info" style="margin-left: 1%;" v-show="cancel" @click="descOrder"><i  class="el-icon-circle-close"></i></el-link>


        </el-col>

    </el-row>
</div>
</template>

<script>

import bus from './eventBus.js';

export default {
    name: "filter",
    data:function () {
        return{
            keywords:"",
            filter:null,


        }
    },
    methods:{
        search(){
            if(this.keywords!=""){
                bus.$emit('filterNote',this.keywords);

            }else{
                this.clear();
            }
        },
        clear(){

                bus.$emit('clearSearch');

        },
        ascOrder(){
            bus.$emit('ascOrder');
        },
        descOrder(){
            this.filter = null;
            bus.$emit('descOrder');
        }
    },
    computed:{
        cancel:function () {
            return this.filter!==null
        },

    },
}
</script>

<style scoped>

</style>