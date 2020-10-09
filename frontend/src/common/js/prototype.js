import config from '@/common/js/config' // 配置文件
import utils from '@/common/js/utils' // 公共方法
import eventBus from '@/common/js/eventBus'

export default {
  install (Vue, options) {
    Vue.prototype.$config = config
    Vue.prototype.$fn = utils
    Vue.prototype.$eventBus = eventBus
  }
}
