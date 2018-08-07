Vue.prototype.$http = axios
var app = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        query: "",
        pages: [],
        detail: null
    },
    computed: {
        noDetail: function(){
            if(this.detail == null){
                return true;
            }else{
                return false;
            }
        }
    },
    methods: {
        search: function(){
            if(this.query == ""){
                return 0;
            }
            var request = {
                "query": this.query
            }
            var self = this;
            self.$http({
                method: "POST",
                url:"/search",
                data: request
            }).then(function(response){
                self.pages = response.data.pages;
            }).catch(function(error){
                console.log(error);
            });
        },
        showDetail: function(page, index){
            var request = {
                "url": page.url,
                "description": page.description
            }
            var self = this;
            self.$http({
                method: "POST",
                url:"/detail",
                data: request
            }).then(function(response){
                self.detail = response.data.detail;
            }).catch(function(error){
                console.log(error);
            });

        }
    }
})
