(window["webpackJsonpls-host-config"]=window["webpackJsonpls-host-config"]||[]).push([[10],{120:function(e,a,t){"use strict";var r=t(127),c=t.n(r).a.create({baseURL:"http://localhost/api/",timeout:1e4,headers:{"ls-token":"1234567890abcdef"}});a.a=c},138:function(e,a,t){"use strict";t.d(a,"a",(function(){return n}));var r=t(23);function c(e,a){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);a&&(r=r.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),t.push.apply(t,r)}return t}function n(e){for(var a=1;a<arguments.length;a++){var t=null!=arguments[a]?arguments[a]:{};a%2?c(Object(t),!0).forEach((function(a){Object(r.a)(e,a,t[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):c(Object(t)).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(t,a))}))}return e}},300:function(e,a,t){"use strict";t.r(a);var r=t(23),c=t(138),n=t(63),l=t(52),o=t(0),m=t.n(o),s=t(152),i=t(1),d=t(2),u=t(7),h=t.n(u),g=t(43),_=t(11),f=t(8),b=t(150),p=t(151),E=t(179),v=t(38),N=t(42),O=["bsPrefix","show","closeLabel","className","children","variant","onClose","dismissible","transition"],C=Object(E.a)("h4");C.displayName="DivStyledAsH4";var y=Object(v.a)("alert-heading",{Component:C}),j=Object(v.a)("alert-link",{Component:N.a}),w={show:!0,transition:b.a,closeLabel:"Close alert"},k=m.a.forwardRef((function(e,a){var t=Object(g.a)(e,{show:"onClose"}),r=t.bsPrefix,c=t.show,n=t.closeLabel,l=t.className,o=t.children,s=t.variant,u=t.onClose,E=t.dismissible,v=t.transition,N=Object(d.a)(t,O),C=Object(f.a)(r,"alert"),y=Object(_.a)((function(e){u&&u(!1,e)})),j=!0===v?b.a:v,w=m.a.createElement("div",Object(i.a)({role:"alert"},j?void 0:N,{ref:a,className:h()(l,C,s&&C+"-"+s,E&&C+"-dismissible")}),E&&m.a.createElement(p.a,{onClick:y,label:n}),o);return j?m.a.createElement(j,Object(i.a)({unmountOnExit:!0},N,{ref:void 0,in:c}),w):c?w:null}));k.displayName="Alert",k.defaultProps=w,k.Link=j,k.Heading=y;var F=k,x=t(62),D=t(180),A=t(153),I=t(126),G=t.n(I),L=t(120);function T(){var e=Object(o.useState)(!1),a=Object(l.a)(e,2),t=a[0],i=a[1],d=Object(o.useState)(!1),u=Object(l.a)(d,2),h=u[0],g=u[1],_=Object(o.useState)(!1),f=Object(l.a)(_,2),b=f[0],p=f[1],E=Object(o.useState)(""),v=Object(l.a)(E,2),N=v[0],O=v[1],C=Object(o.useState)(0),y=Object(l.a)(C,2),j=y[0],w=y[1],k=Object(o.useState)(""),I=Object(l.a)(k,2),T=I[0],S=I[1],P=Object(o.useState)(""),R=Object(l.a)(P,2),B=R[0],H=R[1],J=Object(o.useState)(!0),M=Object(l.a)(J,2),z=M[0],U=M[1],Y=function(){return i(!1)},q=function(){L.a.get("v1/electric-configs/channels").then((function(e){var a=e.data;a.is_succeed&&Z(a.data.channels)})).catch((function(e){console.log(e)}))},K=function(e){U(!1),H(e),g(!0)},Q=function(e){if(""!==e){var a={ch_name:e,ch_temp_read_address:0,ch_leakcurrent_read_address:0,ch_current_read_address:0,current_allowed_range_max:20,current_info_trigger_range:"10-20",current_info_trigger_duration:30,current_alarm_trigger_range:">20",current_alarm_trigger_duration:30,temp_info_trigger_range:"32-40",temp_info_trigger_duration:30,temp_alarm_trigger_range:">40",temp_alarm_trigger_duration:30,leakcurrent_info_trigger_range:"32-40",leakcurrent_info_trigger_duration:30,leakcurrent_alarm_trigger_range:">40",leakcurrent_alarm_trigger_duration:30};console.log("Trying to add new channel: ",a),L.a.post("v1/electric-configs/channels",a).then((function(e){var t,r=e.data;r.is_succeed?(t="\u6dfb\u52a0\u901a\u9053 '".concat(a.ch_name,"' \u6210\u529f\uff01"),U(!0),H(t),g(!0),q()):K("\u6dfb\u52a0\u901a\u9053 '".concat(a.ch_name,"' \u5931\u8d25: ")+r.message)})).catch((function(e){K("\u6dfb\u52a0\u901a\u9053 '".concat(a.ch_name,"' \u5931\u8d25: ")+e.message)}))}else K("\u6dfb\u52a0\u901a\u9053\u5931\u8d25\uff0c\u901a\u9053\u540d\u4e0d\u80fd\u4e3a\u7a7a\uff01")},V=Object(o.useState)([]),W=Object(l.a)(V,2),X=W[0],Z=W[1],$=Object(o.useState)([!1,!1,!1,!1,!1]),ee=Object(l.a)($,2),ae=ee[0],te=ee[1],re=function(e,a,t){var l=[].concat(Object(n.a)(X.slice(0,a)),[Object(c.a)(Object(c.a)({},X[a]),{},Object(r.a)({},t,e.target.value))],Object(n.a)(X.slice(a+1)));Z(l)},ce=function(e,a,t){var l=[].concat(Object(n.a)(X.slice(0,a)),[Object(c.a)(Object(c.a)({},X[a]),{},Object(r.a)({},t,parseInt(e.target.value)))],Object(n.a)(X.slice(a+1)));Z(l)};return Object(o.useEffect)((function(){G.a.init(),q()}),[]),m.a.createElement(m.a.Fragment,null,m.a.createElement(F,{show:h,variant:z?"success":"danger",onClose:function(){return g(!1)},dismissible:!0},m.a.createElement(F.Heading,null,z?"\u64cd\u4f5c\u6210\u529f":"\u64cd\u4f5c\u5931\u8d25"),m.a.createElement("p",null,B)),m.a.createElement("div",{style:{display:"flex",alignItems:"center",justifyContent:"center"}},m.a.createElement(A.a,{onClose:function(){return p(!1)},style:{position:"fixed",zIndex:3,width:"80%"},show:b,delay:1e4,autohide:!0},m.a.createElement(A.a.Header,null,m.a.createElement("strong",{className:"mr-auto"},"\u7535\u7bb1\u914d\u7f6e"),m.a.createElement("small",null,"1 mins ago")),m.a.createElement(A.a.Body,null,N))),m.a.createElement("div",null,m.a.createElement("div",{className:"page-header"},m.a.createElement("h3",{className:"page-title"},"\u7535\u7bb1\u914d\u7f6e")),m.a.createElement("form",{className:"form-inline"},m.a.createElement("label",{className:"sr-only",htmlFor:"inlineFormChannelName"},"Name"),m.a.createElement(s.a.Control,{type:"text",className:"form-control mb-2 mr-sm-2",id:"inlineFormChannelName",value:T,onChange:function(e){S(e.target.value)},placeholder:"\u901a\u9053\u540d\u79f0"}),m.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mb-2",onClick:function(){Q(T)}},"\u6dfb\u52a0\u65b0\u901a\u9053")),m.a.createElement("div",{className:"row mt-5",style:{height:"465px",overflowY:"scroll"}},X.length>0?X.map((function(e,a){return m.a.createElement("div",{className:"col-md-6 grid-margin stretch-card",key:"ch-".concat(e.id)},m.a.createElement("div",{className:"card"},m.a.createElement("div",{className:"card-body"},m.a.createElement("div",{style:{display:"flex",alignItems:"center",justifyContent:"space-between",cursor:"pointer"},onClick:function(){console.log("To remove channel: ",e.ch_name),w(a),i(!0)}},m.a.createElement("h4",{className:"card-title"},m.a.createElement("i",{className:"mdi mdi-flash-auto"}),"\u901a\u9053".concat(a)),m.a.createElement("i",{className:"mdi mdi-delete icon-sm text-primary align-middle"})),m.a.createElement("form",{className:"forms-sample"},m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chId".concat(e.id),className:"col-sm-3 col-form-label"},"ID"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chId-".concat(e.id),placeholder:"",value:e.id,readOnly:!0}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"currentRangeMax".concat(e.id),className:"col-sm-3 col-form-label"},"\u91cf\u7a0b"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{as:"select",id:"currentRangeMax".concat(e.id),className:"mt-2",onChange:function(e){return ce(e,a,"current_allowed_range_max")}},["10","15","20","25"].map((function(a){return m.a.createElement("option",{key:a,value:a,selected:parseInt(a)===e.current_allowed_range_max},a)}))))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chName".concat(e.id),className:"col-sm-3 col-form-label"},"\u901a\u9053\u540d"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chName".concat(e.id),placeholder:"",value:e.ch_name,onChange:function(e){re(e,a,"ch_name")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("button",{type:"button",className:"btn btn-inverse-danger btn-icon",onClick:function(){var e=Object(n.a)(ae);e[a]=!e[a],te(e)}},m.a.createElement("i",{className:ae[a]?"mdi mdi-chevron-double-up":"mdi mdi-chevron-double-down"}))),ae[a]?m.a.createElement(m.a.Fragment,null,m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chTempReadAddress".concat(e.id),className:"col-sm-3 col-form-label"},"\u6e29\u5ea6\u8bfb\u53d6\u5730\u5740"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chTempReadAddress".concat(e.id),placeholder:"",value:e.ch_temp_read_address,onChange:function(e){re(e,a,"ch_temp_read_address")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chLeakCurrentReadAddress".concat(e.id),className:"col-sm-3 col-form-label"},"\u6f0f\u7535\u6d41\u8bfb\u53d6\u5730\u5740"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chLeakCurrentReadAddress".concat(e.id),placeholder:"",value:e.ch_leakcurrent_read_address,onChange:function(e){re(e,a,"ch_leakcurrent_read_address")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chCurrentReadAddress".concat(e.id),className:"col-sm-3 col-form-label"},"\u7535\u6d41\u8bfb\u53d6\u5730\u5740"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chCurrentReadAddress".concat(e.id),placeholder:"",value:e.ch_current_read_address,onChange:function(e){re(e,a,"ch_current_read_address")}}))),m.a.createElement("div",{className:"mt-1 mb-1",style:{width:"100%",height:"1px",backgroundColor:"#78BDF5"}}),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverTempInfo".concat(e.id),className:"col-sm-3 col-form-label"},"\u8fc7\u70ed\u89e6\u53d1\uff08\u63d0\u793a\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chOverTempInfo".concat(e.id),placeholder:"",value:e.temp_info_trigger_range,onChange:function(e){re(e,a,"temp_info_trigger_range")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverTempInfoDuration".concat(e.id),className:"col-sm-3 col-form-label"},"\u89e6\u53d1\u65f6\u95f4\uff08\u79d2\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chOverTempInfoDuration".concat(e.id),placeholder:"250",value:e.temp_info_trigger_duration,onChange:function(e){ce(e,a,"temp_info_trigger_duration")}}))),m.a.createElement("div",{className:"mt-1 mb-1",style:{width:"100%",height:"1px",backgroundColor:"#78BDF5"}}),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverTempAlarm".concat(e.id),className:"col-sm-3 col-form-label"},"\u8fc7\u70ed\u89e6\u53d1(\u544a\u8b66)"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chOverTempAlarm".concat(e.id),placeholder:"",value:e.temp_alarm_trigger_range,onChange:function(e){re(e,a,"temp_alarm_trigger_range")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverTempAlarmDuration".concat(e.id),className:"col-sm-3 col-form-label"},"\u89e6\u53d1\u65f6\u95f4(\u79d2)"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chOverTempAlarmDuration".concat(e.id),placeholder:"250",value:e.temp_alarm_trigger_duration,onChange:function(e){ce(e,a,"temp_alarm_trigger_duration")}}))),m.a.createElement("div",{className:"mt-1 mb-1",style:{width:"100%",height:"1px",backgroundColor:"#78BDF5"}}),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverCurrentInfo".concat(e.id),className:"col-sm-3 col-form-label"},"\u8fc7\u6d41\u89e6\u53d1\uff08\u63d0\u793a\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chOverCurrentInfo".concat(e.id),placeholder:"",value:e.current_info_trigger_range,onChange:function(e){re(e,a,"current_info_trigger_range")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverCurrentInfoDuration".concat(e.id),className:"col-sm-3 col-form-label"},"\u89e6\u53d1\u65f6\u95f4\uff08\u79d2\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chOverCurrentInfoDuration".concat(e.id),placeholder:"250",value:e.current_info_trigger_duration,onChange:function(e){ce(e,a,"current_info_trigger_duration")}}))),m.a.createElement("div",{className:"mt-1 mb-1",style:{width:"100%",height:"1px",backgroundColor:"#78BDF5"}}),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverCurrentAlarm".concat(e.id),className:"col-sm-3 col-form-label"},"\u8fc7\u6d41\u89e6\u53d1\uff08\u544a\u8b66\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chOverCurrentAlarm".concat(e.id),placeholder:"",value:e.current_alarm_trigger_range,onChange:function(e){re(e,a,"current_alarm_trigger_range")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverCurrentAlarmDuration".concat(e.id),className:"col-sm-3 col-form-label"},"\u89e6\u53d1\u65f6\u95f4\uff08\u79d2\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chOverCurrentAlarmDuration".concat(e.id),placeholder:"250",value:e.current_alarm_trigger_duration,onChange:function(e){ce(e,a,"current_alarm_trigger_duration")}}))),m.a.createElement("div",{className:"mt-1 mb-1",style:{width:"100%",height:"1px",backgroundColor:"#78BDF5"}}),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverLeakCurrentInfo".concat(e.id),className:"col-sm-3 col-form-label"},"\u6f0f\u7535\u6d41\uff08\u63d0\u793a\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chOverLeakCurrentInfo".concat(e.id),placeholder:"250",value:e.leakcurrent_info_trigger_range,onChange:function(e){re(e,a,"leakcurrent_info_trigger_range")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverLeakCurrentInfoDuration".concat(e.id),className:"col-sm-3 col-form-label"},"\u89e6\u53d1\u65f6\u95f4\uff08\u79d2\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chOverLeakCurrentInfoDuration".concat(e.id),placeholder:"250",value:e.leakcurrent_info_trigger_duration,onChange:function(e){ce(e,a,"leakcurrent_info_trigger_duration")}}))),m.a.createElement("div",{className:"mt-1 mb-1",style:{width:"100%",height:"1px",backgroundColor:"#78BDF5"}}),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverLeakCurrentAlarm".concat(e.id),className:"col-sm-3 col-form-label"},"\u6f0f\u7535\u6d41\uff08\u544a\u8b66\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"text",className:"form-control",id:"chOverLeakCurrentAlarm".concat(e.id),placeholder:"250",value:e.leakcurrent_alarm_trigger_range,onChange:function(e){re(e,a,"leakcurrent_alarm_trigger_range")}}))),m.a.createElement(s.a.Group,{className:"row"},m.a.createElement("label",{htmlFor:"chOverLeakCurrentAlarmDuration".concat(e.id),className:"col-sm-3 col-form-label"},"\u89e6\u53d1\u65f6\u95f4\uff08\u79d2\uff09"),m.a.createElement("div",{className:"col-sm-9"},m.a.createElement(s.a.Control,{type:"number",className:"form-control",id:"chOverLeakCurrentAlarmDuration".concat(e.id),placeholder:"250",value:e.leakcurrent_alarm_trigger_duration,onChange:function(e){ce(e,a,"leakcurrent_alarm_trigger_duration")}})))):null,m.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){!function(e){var a=X[e];console.log("Trying to update channel: ",a),L.a.put("v1/electric-configs/channels/".concat(a.id),a).then((function(e){e.data.is_succeed?(q(),O("\u66f4\u65b0\u901a\u9053 '".concat(a.ch_name,"' \u6210\u529f\uff01")),p(!0)):(O("\u66f4\u65b0\u901a\u9053 '".concat(a.ch_name,"' \u5931\u8d25\uff01")),p(!0))})).catch((function(e){O("\u66f4\u65b0\u901a\u9053 '".concat(a.ch_name,"' \u5931\u8d25\uff01")),p(!0)}))}(a)}},"\u786e\u5b9a")))))})):"\u6ca1\u6709\u901a\u9053\u53ef\u663e\u793a\uff01")),m.a.createElement(D.a,{show:t,onHide:Y},m.a.createElement(D.a.Header,{closeButton:!0},m.a.createElement(D.a.Title,null,"\u8b66\u544a")),m.a.createElement(D.a.Body,null,X.length>0&&j>=0&&j<X.length?"\u5373\u5c06\u5220\u9664\u901a\u9053\uff1a".concat(X[j].ch_name,"\uff0c\u662f\u5426\u7ee7\u7eed"):""),m.a.createElement(D.a.Footer,null,m.a.createElement(x.a,{variant:"secondary",onClick:Y},"\u53d6\u6d88"),m.a.createElement(x.a,{variant:"primary",onClick:function(){var e;e=j,Y(),L.a.delete("v1/electric-configs/channels/".concat(X[e].id)).then((function(a){var t=a.data;t.is_succeed?(O("\u5220\u9664\u901a\u9053 '".concat(X[e].ch_name,"' \u6210\u529f\uff01")),p(!0),q()):(console.log("\u5220\u9664\u901a\u9053 '".concat(X[e].ch_name,"' \u5931\u8d25: ")+t.message),O("\u5220\u9664\u901a\u9053 '".concat(X[e].ch_name,"' \u5931\u8d25\uff01")),p(!0))})).catch((function(a){console.log("\u5220\u9664\u901a\u9053 '".concat(X[e].ch_name,"' \u5931\u8d25: ")+a.message),O("\u5220\u9664\u901a\u9053 '".concat(X[e].ch_name,"' \u5931\u8d25\uff01")),p(!0)}))}},"\u786e\u5b9a"))))}t.d(a,"default",(function(){return T}))}}]);
//# sourceMappingURL=10.aa462e94.chunk.js.map