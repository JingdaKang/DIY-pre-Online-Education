import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Register from '@/components/Register'
import Home from '@/components/Home'
import User from '@/components/User'
import Password from '@/components/Password'
import Admin from '@/components/Admin'
import Account from '@/components/Account'
import Class from '@/components/Class'
import Message from '@/components/Message'
import AllClass from '@/components/AllClass'
import ClassManage from '@/components/ClassManage'
import ReleaseClass from '@/components/ReleaseClass'
import MyClass from '@/components/MyClass'
import SelectedClass from '@/components/SelectedClass'
import ClassDetail from '@/components/ClassDetail'
import ForgetPassword from '@/components/ForgetPassword'


import AddRelease from '@/IAsystem/AddRelease'
import MyResource from '@/IAsystem/MyResource'
import IAsystem from '@/IAsystem/IAsystem'
import Search from '@/IAsystem/Search'
import ReleaseHall from '@/IAsystem/ReleaseHall'
import MyRelease from '@/IAsystem/MyRelease'
import Question from '@/IAsystem/Question'
import Request from '@/IAsystem/Request'
import MyAnswer from '@/IAsystem/MyAnswer'


import ExamTeacher from '../exam/ExamTeacher'
import ExamStudent from '../exam/ExamStudent'
import AddQuestion from '../exam/AddQuestion'
import SelectQuestion from '../exam/SelectQuestion'
import ChooseQuestion from '../exam/ChooseQuestion'
import AddPaper from '../exam/AddPaper'
import AddExam from '../exam/AddExam'
import SelectExam from '../exam/SelectExam'
import DoExam from '../exam/DoExam'
import ShowQuestion from '../exam/ShowQuestion'
import SelectScore from '../exam/SelectScore'
import ShowAnswer from '../exam/ShowAnswer'
import ShowScore from '../exam/ShowScore'
import SetCourse from '../exam/SetCourse'
import ShowGrade from '../exam/ShowGrade'
import StudentScore from '../exam/StudentScore'
import FindWrong from '../exam/FindWrong'
import SelectPaper from '../exam/SelectPaper'
import ShowPaper from '../exam/ShowPaper'
import FindExam from '../exam/FindExam'
import ShowExam from '../exam/ShowExam'
import AddTest from '../exam/AddTest'
import StudentGrade from '../exam/StudentGrade'
import AddSection from '../exam/AddSection'

import Forum from '@/forum/Forum'
import Forum_Home from '@/forum/home/Home'
import SectionIndex from '@/forum/section/SectionIndex'
import SearchList from '@/forum/search/SearchList'
import NewTopic from '@/forum/topic/NewTopic'
import EditTopic from '@/forum/topic/EditTopic'
import UserInfo from '@/forum/user/UserInfo'
import TopicInfo from '@/forum/topic/TopicInfo'
import Group from '@/forum/group/Group'
import DiscussInfo from '@/forum/group/DiscussInfo'
import EditDiscuss from '@/forum/group/EditDiscuss'
import NewDiscuss from '@/forum/group/NewDiscuss'
import UserHome from '@/forum/user/UserHome'
import UserTopic from '@/forum/user/UserTopic'
import UserTopicReply from '@/forum/user/UserTopicReply'
import UserDiscuss from '@/forum/user/UserDiscuss'
import UserDiscussReply from '@/forum/user/UserDiscussReply'
import UserCollect from '@/forum/user/UserCollect'
import UserFollowing from '@/forum/user/UserFollowing'
import UserFollower from '@/forum/user/UserFollower'
import UserFocus from '@/forum/user/UserFocus'
import UserMessage from '@/forum/user/UserMessage'
import UserApply from '@/forum/user/UserApply'
import QuestionPage from '@/forum/QuestionPage'

import Student from '@/work/Student'
import Teacher from '@/work/Teacher'
import AllCourse from '@/work/Student/AllCourse'
import MyWork from '@/work/Student/MyWork'
import WrongQuestions from '@/work/Student/WrongQuestions'
import Material from '@/work/Student/Material'
import GoodWork from '@/work/Student/GoodWork'
import MyCourse from '@/work/Student/MyCourse'
import Course_Work from '@/work/Teacher/Course_Work'
import TMaterial from '@/work/Teacher/TMaterial'
import TGoodWork from '@/work/Teacher/TGoodWork'
import Student_Course from '@/work/Teacher/Student_Course'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home
    },
    {
      path: '/User',
      name: 'User',
      component: User
    },
    {
      path: '/Password',
      name: 'Password',
      component: Password
    },
    {
      path: '/ForgetPassword',
      name: 'ForgetPassword',
      component: ForgetPassword
    },
    {
      path: '/Admin',
      name: 'Admin',
      component: Admin,
      meta: {
        keepAlive: true,
      },
      children: [
        {
          path: '',
          component: Account,
        },
        {
          path: '/Account',
          name: 'Account',
          component: Account,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/Class',
          name: 'Class',
          component: Class,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/Message',
          name: 'Message',
          component: Message,
          meta: {
            keepAlive: true,
          }
        },
      ]
    },

    {
      path: '/ClassManage',
      name: 'ClassManage',
      component: ClassManage,
      meta: {
        keepAlive: true,
      },
      children: [
        {
          path: '',
          component: AllClass,
        },
        {
          path: '/ReleaseClass',
          name: 'ReleaseClass',
          component: ReleaseClass,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/MyClass',
          name: 'MyClass',
          component: MyClass,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/SelectedClass',
          name: 'SelectedClass',
          component: SelectedClass,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/ClassDetail/:id',
          name: 'ClassDetail',
          component: ClassDetail
        },
        {
          path: '/AllClass',
          name: 'AllClass',
          component: AllClass,
          meta: {
            keepAlive: true,
          }
        },
      ]
    },


//智能问答页面

     {
      path: '/IAsystem',
      name: 'IAsystem',
      component: IAsystem,
      children: [
        {
          path: '',
          component: Search,
        },

        {
          path: '/AddRelease',
          name: 'AddRelease',
          component: AddRelease,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/MyAnswer',
          name: 'MyAnswer',
          component: MyAnswer,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/MyResource',
          name: 'MyResource',
          component: MyResource,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/Search',
          name: 'Search',
          component: Search,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/ReleaseHall',
          name: 'ReleaseHall',
          component: ReleaseHall,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/MyRelease',
          name: 'MyRelease',
          component: MyRelease,
          meta: {
            keepAlive: true,
          }
        },
        {
          path: '/Question/:question_id',
          name: 'Question',
        component: Question
      },
      {
        path: '/Request/:request_id',
        name: 'Request',
        component: Request
      }
      ]
    },

// 考试相关页面
        {
          path: '/exam/teacher',
          name: 'ExamTeacher',
          component: ExamTeacher,
          children: [{
            path: '/addQuestion',
            name: 'AddQuestion',
            component: AddQuestion
          },
          {
            path: '/selectQuestion',
            name: 'SelectQuestion',
            component: SelectQuestion
          },
          {
            path: '/addPaper',
            name: 'AddPaper',
            component: AddPaper
          },
          {
            path: '/chooseQuestion',
            name: 'ChooseQuestion',
            component: ChooseQuestion
          },
          {
            path: '/selectPaper',
            name: 'SelectPaper',
            component: SelectPaper
          },
          {
            path: '/showPaper',
            name: 'ShowPaper',
            component: ShowPaper
          },
          {
            path: '/addExam',
            name: 'AddExam',
            component: AddExam
          },
          {
            path: '/selectScore',
            name: 'SelectScore',
            component: SelectScore
          },
          {
            path: '/showAnswer',
            name: 'ShowAnswer',
            component: ShowAnswer
          },
          {
            path: '/showScore',
            name: 'ShowScore',
            component: ShowScore
          },
          {
            path: '/setCourse',
            name: 'SetCourse',
            component: SetCourse
          },
          {
            path: '/showGrade',
            name: 'ShowGrade',
            component: ShowGrade
          },
          {
            path: '/findExam',
            name: 'FindExam',
            component: FindExam
          },
          {
            path: '/showExam',
            name: 'ShowExam',
            component: ShowExam
          }]
        },
        {
          path: '/exam/student',
          name: 'ExamStudent',
          component: ExamStudent,
          children: [{
            path: '/selectExam',
            name: 'SelectExam',
            component: SelectExam
          },
          {
            path: '/doExam',
            name: 'DoExam',
            component: DoExam
          },
          {
            path: '/showQuestion',
            name: 'ShowQuestion',
            component: ShowQuestion
          },
          {
            path: '/studentScore',
            name: 'StudentScore',
            component: StudentScore
          },
          {
            path: '/findWrong',
            name: 'FindWrong',
            component: FindWrong
          },
          {
            path: '/addTest',
            name: 'AddTest',
            component: AddTest
          },
          {
            path: '/studentGrade',
            name: 'StudentGrade',
            component: StudentGrade
          }]
        },
        {
          path: '/addSection',
          name: 'AddSection',
          component: AddSection
        },

        // 论坛相关
     {
      path: '/forum_home',
      name: 'forum',
      component: Forum,
      children:[
       {
          path: '',
          component: Forum_Home,
        },
      {
      path: '/forum',
      name: 'home',
      component: Forum_Home

    },
    {
      path: '/forum/section',
      name: 'SectionIndex',
      component: SectionIndex
    },
    {
      path: '/forum/search',
      name: 'SearchList',
      component: SearchList
    },
    {
      path: '/forum/newtopic',
      name: 'NewTopic',
      component: NewTopic
    },
    {
      path: '/forum/topic/:id',
      name: 'TopicInfo',
      component: TopicInfo
    },
    {
      path: '/forum/editTopic/:id',
      name: 'EditTopic',
      component: EditTopic
    },
    {
      path: '/forum/group',
      name: 'Group',
      component: Group
    },
    {
      path: '/forum/newdiscuss',
      name: 'NewDiscuss',
      component: NewDiscuss
    },
    {
      path: '/forum/discuss/:id',
      name: 'DiscussInfo',
      component: DiscussInfo
    },
    {
      path: '/forum/editDiscuss/:id',
      name: 'EditDiscuss',
      component: EditDiscuss
    },

    {
      path: '/forum/userhome',
      name: 'UserHome',
      component: UserHome,
      children:[
        {
          path:'/forum/userhome',
          name:'UserTopic',
          component:UserTopic
        },
        {
          path:'/forum/userhome/info',
          name:'UserInfo',
          component:UserInfo
        },
        {
          path:'/forum/userhome/topic',
          name:'UserTopic',
          component:UserTopic
        },
        {
          path:'/forum/userhome/reply',
          name:'UserTopicReply',
          component:UserTopicReply
        },
        {
          path:'/forum/userhome/discuss',
          name:'UserDiscuss',
          component:UserDiscuss
        },
        {
          path:'/forum/userhome/discussreply',
          name:'UserDiscussReply',
          component:UserDiscussReply
        },
        {
          path:'/forum/userhome/collect',
          name:'UserCollect',
          component:UserCollect
        },
        {
          path:'/forum/userhome/following',
          name:'UserFollowing',
          component:UserFollowing
        },
        {
          path:'/forum/userhome/follower',
          name:'UserFollower',
          component:UserFollower
        },
        {
          path:'/forum/userhome/focus',
          name:'UserFocus',
          component:UserFocus
        },
        {
          path:'/forum/userhome/message',
          name:'UserMessage',
          component:UserMessage
        },
        {
          path:'/forum/userhome/apply',
          name:'UserApply',
          component:UserApply
        },
      ]
    },
    {
      path: '/forum/questionpage',
      name: 'QuestionPage',
      component: QuestionPage
    },
      ]
 },

 //作业相关
    {
      path: '/work/Student',
      name: 'Student',
      component: Student,
      children:[
        {
          path: '/Student/MyCourse',
          name: 'MyCourse',
          component: MyCourse
        },
        {
          path: '/Student/AllCourse',
          name: 'AllCourse',
          component: AllCourse
        },
        {
          path: '/Student/MyWork',
          name: 'MyWork',
          component: MyWork
        },
        {
          path: '/Student/WrongQuestions',
          name: 'WrongQuestions',
          component: WrongQuestions
        },
        {
          path: '/Student/Material',
          name: 'Material',
          component: Material
        },
        {
          path: '/Student/GoodWork',
          name: 'GoodWork',
          component: GoodWork
        }
      ]
    },
    {
      path: '/work/Teacher',
      name: 'Teacher',
      component: Teacher,
      children:[
        {
          path: '/Teacher/Course_Work',
          name: 'Course_Work',
          component: Course_Work
        },
        {
          path: '/Teacher/TMaterial',
          name: 'TMaterial',
          component: TMaterial
        },
        {
          path: '/Teacher/TGoodWork',
          name: 'TGoodWork',
          component: TGoodWork
        },
        {
          path: '/Teacher/Student_Course',
          name: 'Student_Course',
          component: Student_Course
        },
      ]
    },
    //云笔记
    {
    name:"cloudnote",
    path:"/cloudnote",
    component:()=>import("../cloudnote/cloudnote.vue"),
    children:[
    {
     name:"main",
    path:"",
    component:()=>import("../cloudnote/pages/Main.vue"),
    },
     {
    name:"main",
    path:"/main",
    component:()=>import("../cloudnote/pages/Main.vue"),
    children:[
    {
        name:'main',
        path:'',
        component:()=>import("../cloudnote/pages/write/write.vue")
    },
    {
        name:"files",
        path:"files",
        component:()=>import("../cloudnote/pages/files/files.vue")
    },
    {
        name:"write",
        path:"write",
        component:()=>import("../cloudnote/pages/write/write.vue")
    },
    {
        name:"rubbish",
        path:"rubbish",
        component:()=>import("../cloudnote/pages/rubbish/rubbish.vue")
    },
    {
        name:"team",
        path:"team",
        component:()=>import("../cloudnote/pages/team/Team.vue")
    },
    {
        name:"manage",
        path:"manage",
        component:()=>import("../cloudnote/pages/manage/manage.vue"),
    },
    {
        name:"tag",
        path:"tag",
        component:()=>import("../cloudnote/pages/tag/Tag.vue"),
    },
    {
        name:"notice",
        path:"notice",
        component:()=>import("../cloudnote/pages/notice/Notice.vue"),
    },
    ]
},
    ]
    }

]
})
