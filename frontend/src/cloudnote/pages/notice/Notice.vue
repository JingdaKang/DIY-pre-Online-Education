<template>
    <div style="padding-left: 2%;padding-right:2%">

<!--导航-->

         <navigate ref="navigate"></navigate>




<!--        通知列表-->
        <notice-list ref="NoticeList"></notice-list>




    </div>
</template>

<script>


    import Navigate from "@/cloudnote/pages/notice/components/navigate";
    import NoticeList from "@/cloudnote/pages/notice/components/notice-list";
    export default {

        name: "team",
        data:function () {
            return{



            }
        },
        methods:{

        },

        components:{
            NoticeList,
            Navigate,

        }


    }
</script>

<style scoped>

</style>
