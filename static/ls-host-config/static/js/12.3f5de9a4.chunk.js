(window["webpackJsonpls-host-config"]=window["webpackJsonpls-host-config"]||[]).push([[12],{149:function(e,a,t){e.exports=t.p+"static/media/circle.1541da91.svg"},295:function(e,a,t){"use strict";t.r(a),t.d(a,"Dashboard",(function(){return u}));var l=t(62),r=t(139),n=t(15),c=t(16),d=t(65),s=t(18),i=t(17),o=t(0),m=t.n(o),g=t(180),u=function(e){Object(s.a)(o,e);var a=Object(i.a)(o);function o(e){var t;return Object(n.a)(this,o),(t=a.call(this,e)).handleChange=function(e){t.setState({startDate:e})},t.state={startDate:new Date,visitSaleData:{},visitSaleOptions:{scales:{yAxes:[{ticks:{beginAtZero:!0,display:!1,min:0,stepSize:20,max:80},gridLines:{drawBorder:!1,color:"rgba(235,237,242,1)",zeroLineColor:"rgba(235,237,242,1)"}}],xAxes:[{gridLines:{display:!1,drawBorder:!1,color:"rgba(0,0,0,1)",zeroLineColor:"rgba(235,237,242,1)"},ticks:{padding:20,fontColor:"#9c9fa6",autoSkip:!0},categoryPercentage:.5,barPercentage:.5}]},legend:{display:!1},elements:{point:{radius:0}}},trafficData:{},trafficOptions:{responsive:!0,animation:{animateScale:!0,animateRotate:!0},legend:!1},todos:[{id:1,task:"Pick up kids from school",isCompleted:!1},{id:2,task:"Prepare for presentation",isCompleted:!0},{id:3,task:"Print Statements",isCompleted:!1},{id:4,task:"Create invoice",isCompleted:!1},{id:5,task:"Call John",isCompleted:!0},{id:6,task:"Meeting with Alisa",isCompleted:!1}],inputValue:""},t.statusChangedHandler=t.statusChangedHandler.bind(Object(d.a)(t)),t.addTodo=t.addTodo.bind(Object(d.a)(t)),t.removeTodo=t.removeTodo.bind(Object(d.a)(t)),t.inputChangeHandler=t.inputChangeHandler.bind(Object(d.a)(t)),t}return Object(c.a)(o,[{key:"statusChangedHandler",value:function(e,a){var t=Object(r.a)({},this.state.todos[a]);t.isCompleted=e.target.checked;var n=Object(l.a)(this.state.todos);n[a]=t,this.setState({todos:n})}},{key:"addTodo",value:function(e){e.preventDefault();var a=Object(l.a)(this.state.todos);a.unshift({id:a.length?a[a.length-1].id+1:1,task:this.state.inputValue,isCompleted:!1}),this.setState({todos:a,inputValue:""})}},{key:"removeTodo",value:function(e){var a=Object(l.a)(this.state.todos);a.splice(e,1),this.setState({todos:a})}},{key:"inputChangeHandler",value:function(e){this.setState({inputValue:e.target.value})}},{key:"componentDidMount",value:function(){var e=document.getElementById("visitSaleChart").getContext("2d"),a=e.createLinearGradient(0,0,0,181);a.addColorStop(0,"rgba(218, 140, 255, 1)"),a.addColorStop(1,"rgba(154, 85, 255, 1)");var t=e.createLinearGradient(0,0,0,360);t.addColorStop(0,"rgba(54, 215, 232, 1)"),t.addColorStop(1,"rgba(177, 148, 250, 1)");var l=e.createLinearGradient(0,0,0,300);l.addColorStop(0,"rgba(255, 191, 150, 1)"),l.addColorStop(1,"rgba(254, 112, 150, 1)");var r=e.createLinearGradient(0,0,0,181);r.addColorStop(0,"rgba(54, 215, 232, 1)"),r.addColorStop(1,"rgba(177, 148, 250, 1)");var n=e.createLinearGradient(0,0,0,50);n.addColorStop(0,"rgba(6, 185, 157, 1)"),n.addColorStop(1,"rgba(132, 217, 210, 1)");var c=e.createLinearGradient(0,0,0,300);c.addColorStop(0,"rgba(254, 124, 150, 1)"),c.addColorStop(1,"rgba(255, 205, 150, 1)");var d={labels:["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG"],datasets:[{label:"CHN",borderColor:a,backgroundColor:a,hoverBackgroundColor:a,legendColor:a,pointRadius:0,fill:!1,borderWidth:1,data:[20,40,15,35,25,50,30,20]},{label:"USA",borderColor:t,backgroundColor:t,hoverBackgroundColor:t,legendColor:t,pointRadius:0,fill:!1,borderWidth:1,data:[40,30,20,10,50,15,35,40]},{label:"UK",borderColor:l,backgroundColor:l,hoverBackgroundColor:l,legendColor:l,pointRadius:0,fill:!1,borderWidth:1,data:[70,10,30,40,25,50,15,30]}]},s={datasets:[{data:[30,30,40],backgroundColor:[r,n,c],hoverBackgroundColor:[r,n,c],borderColor:[r,n,c],legendColor:[r,n,c]}],labels:["Search Engines","Direct Click","Bookmarks Click"]};this.setState({visitSaleData:d,trafficData:s})}},{key:"toggleProBanner",value:function(){document.querySelector(".proBanner").classList.toggle("hide")}},{key:"render",value:function(){return m.a.createElement("div",null,m.a.createElement("div",{className:"page-header"},m.a.createElement("h3",{className:"page-title"},m.a.createElement("span",{className:"page-title-icon bg-gradient-primary text-white mr-2"},m.a.createElement("i",{className:"mdi mdi-home"}))," \u4e3b\u9875 "),m.a.createElement("nav",{"aria-label":"breadcrumb"},m.a.createElement("ul",{className:"breadcrumb"},m.a.createElement("li",{className:"breadcrumb-item active","aria-current":"page"},m.a.createElement("span",null),"\u6982\u89c8 ",m.a.createElement("i",{className:"mdi mdi-alert-circle-outline icon-sm text-primary align-middle"}))))),m.a.createElement("div",{className:"row"},m.a.createElement("div",{className:"col-md-4 stretch-card grid-margin"},m.a.createElement("div",{className:"card bg-gradient-danger card-img-holder text-white"},m.a.createElement("div",{className:"card-body"},m.a.createElement("img",{src:t(149),className:"card-img-absolute",alt:"circle"}),m.a.createElement("h4",{className:"font-weight-normal mb-3"},"CPU",m.a.createElement("i",{className:"mdi mdi-chart-line mdi-24px float-right"})),m.a.createElement("h2",{className:"mb-5"},"30%")))),m.a.createElement("div",{className:"col-md-4 stretch-card grid-margin"},m.a.createElement("div",{className:"card bg-gradient-info card-img-holder text-white"},m.a.createElement("div",{className:"card-body"},m.a.createElement("img",{src:t(149),className:"card-img-absolute",alt:"circle"}),m.a.createElement("h4",{className:"font-weight-normal mb-3"},"\u5185\u5b58",m.a.createElement("i",{className:"mdi mdi-bookmark-outline mdi-24px float-right"})),m.a.createElement("h2",{className:"mb-5"},"250M/1024M")))),m.a.createElement("div",{className:"col-md-4 stretch-card grid-margin"},m.a.createElement("div",{className:"card bg-gradient-success card-img-holder text-white"},m.a.createElement("div",{className:"card-body"},m.a.createElement("img",{src:t(149),className:"card-img-absolute",alt:"circle"}),m.a.createElement("h4",{className:"font-weight-normal mb-3"},"\u7f51\u901f",m.a.createElement("i",{className:"mdi mdi-diamond mdi-24px float-right"})),m.a.createElement("h2",{className:"mb-5"},"1.5Mbps/1.8Mbps"))))),m.a.createElement("div",{className:"row"},m.a.createElement("div",{className:"col-md-7 grid-margin stretch-card"},m.a.createElement("div",{className:"card"},m.a.createElement("div",{className:"card-body"},m.a.createElement("div",{className:"clearfix mb-4"},m.a.createElement("h4",{className:"card-title float-left"},"\u8fdb\u7a0b"),m.a.createElement("div",{id:"visit-sale-chart-legend",className:"rounded-legend legend-horizontal legend-top-right float-right"},m.a.createElement("ul",null,m.a.createElement("li",null,m.a.createElement("span",{className:"legend-dots bg-primary"}),"TKTMesh"),m.a.createElement("li",null,m.a.createElement("span",{className:"legend-dots bg-danger"}),"TKTMeshAgent"),m.a.createElement("li",null,m.a.createElement("span",{className:"legend-dots bg-info"}),"TKTVideoServer")))),m.a.createElement(g.Bar,{ref:"chart",className:"chartLegendContainer",data:this.state.visitSaleData,options:this.state.visitSaleOptions,id:"visitSaleChart"})))),m.a.createElement("div",{className:"col-md-5 grid-margin stretch-card"},m.a.createElement("div",{className:"card"},m.a.createElement("div",{className:"card-body"},m.a.createElement("h4",{className:"card-title"},"\u78c1\u76d8\u7a7a\u95f4"),m.a.createElement(g.Doughnut,{data:this.state.trafficData,options:this.state.trafficOptions}),m.a.createElement("div",{id:"traffic-chart-legend",className:"rounded-legend legend-vertical legend-bottom-left pt-4"},m.a.createElement("ul",null,m.a.createElement("li",null,m.a.createElement("span",{className:"legend-dots bg-info"}),"\u7cfb\u7edf",m.a.createElement("span",{className:"float-right"},"30%")),m.a.createElement("li",null,m.a.createElement("span",{className:"legend-dots bg-success"}),"\u5269\u4f59",m.a.createElement("span",{className:"float-right"},"30%")),m.a.createElement("li",null,m.a.createElement("span",{className:"legend-dots bg-danger"}),"\u5e94\u7528",m.a.createElement("span",{className:"float-right"},"40%")))))))),m.a.createElement("div",{className:"row"},m.a.createElement("div",{className:"col-12 grid-margin"},m.a.createElement("div",{className:"card"},m.a.createElement("div",{className:"card-body"},m.a.createElement("h4",{className:"card-title"},"\u8bbe\u5907"),m.a.createElement("div",{className:"table-responsive"},m.a.createElement("table",{className:"table"},m.a.createElement("thead",null,m.a.createElement("tr",null,m.a.createElement("th",null,"ID"),m.a.createElement("th",null,"\u7c7b\u578b"),m.a.createElement("th",null,"\u8bbe\u5907\u540d"),m.a.createElement("th",null,"\u72b6\u6001"),m.a.createElement("th",null,"\u6570\u636e"),m.a.createElement("th",null,"\u6700\u540e\u66f4\u65b0\u65e5\u671f"))),m.a.createElement("tbody",null,m.a.createElement("tr",null,m.a.createElement("td",null," TEMP.202 "),m.a.createElement("td",null," \u73af\u5883\u6e29\u6e7f\u5ea6\u4f20\u611f\u5668 "),m.a.createElement("td",null," \u529e\u516c\u5ba4201\u6e29\u6e7f\u5ea6 "),m.a.createElement("td",null,m.a.createElement("label",{className:"badge badge-gradient-success"},"\u5728\u7ebf")),m.a.createElement("td",null," TEMP: 32.5, HUM: 62% "),m.a.createElement("td",null," 2023/05/21 12:30:12.5 ")),m.a.createElement("tr",null,m.a.createElement("td",null,"CO1.102"),m.a.createElement("td",null," \u4e00\u6c27\u5316\u78b3\u4f20\u611f\u5668 "),m.a.createElement("td",null," \u53a8\u623f\u5927\u5385 "),m.a.createElement("td",null,m.a.createElement("label",{className:"badge badge-gradient-danger"},"\u79bb\u7ebf")),m.a.createElement("td",null," CO1: 25ppb "),m.a.createElement("td",null," 2023/05/21 12:32:12.5 ")),m.a.createElement("tr",null,m.a.createElement("td",null,"CUR.101 "),m.a.createElement("td",null," \u7535\u6d41\u4f20\u611f\u5668 "),m.a.createElement("td",null," \u53a8\u623f\u51b0\u7bb1\u7ebf\u8def "),m.a.createElement("td",null,m.a.createElement("label",{className:"badge badge-gradient-success"},"\u5728\u7ebf")),m.a.createElement("td",null," CURRENT: 1.2A "),m.a.createElement("td",null," 2023/05/21 12:31:23.5 "))))))))))}}]),o}(o.Component);a.default=u}}]);
//# sourceMappingURL=12.3f5de9a4.chunk.js.map