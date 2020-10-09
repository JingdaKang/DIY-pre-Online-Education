<template>
    <div style="padding-left: 2%;padding-right:2%">

<!--导航-->

         <navigate ref="Navigate"></navigate>




<!--        列表-->
        <team-list ref="TeamList"></team-list>




    </div>
</template>

<script>


    import Navigate from "@/cloudnote/pages/team/components/navigate";
    import TeamList from "@/cloudnote/pages/team/components/team-list";
    export default {

        name: "team",
        data:function () {
            return{



            }
        },
        methods:{

        },

        components:{
            TeamList,
            Navigate,

        }


    }
</script>

<style scoped>

</style>
