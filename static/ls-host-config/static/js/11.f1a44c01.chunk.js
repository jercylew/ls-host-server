(window["webpackJsonpls-host-config"]=window["webpackJsonpls-host-config"]||[]).push([[11],{120:function(e,a,t){"use strict";var l=t(127),c=t.n(l).a.create({baseURL:"/api/",timeout:1e4,headers:{"ls-token":"1234567890abcdef"}});a.a=c},124:function(e,a,t){"use strict";t.d(a,"a",(function(){return l}));var l=function(){return([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,(function(e){return(e^crypto.getRandomValues(new Uint8Array(1))[0]&15>>e/4).toString(16)}))}},299:function(e,a,t){"use strict";t.r(a),t.d(a,"default",(function(){return b}));var l=t(52),c=t(0),r=t.n(c),n=t(4),s=t(39),o=t(152),m=t(126),i=t.n(m),d=t(120),u=t(153),p=t(180),E=t(62);t(124);var f=0,v=1,h=0,N=1;Object(s.a)();function b(){!function(){var e=Object(n.g)().search;r.a.useMemo((function(){return new URLSearchParams(e)}),[e])}();var e=Object(c.useState)(!1),a=Object(l.a)(e,2),t=a[0],s=a[1],m=Object(c.useState)(!1),b=Object(l.a)(m,2),g=b[0],C=b[1],j=Object(c.useState)(""),O=Object(l.a)(j,2),y=O[0],w=O[1],_=Object(c.useState)(""),S=Object(l.a)(_,2),I=S[0],P=S[1],x=Object(c.useState)(""),G=Object(l.a)(x,2),k=G[0],F=G[1],U=Object(c.useState)(""),R=Object(l.a)(U,2),B=R[0],H=R[1],A=Object(c.useState)(""),X=Object(l.a)(A,2),J=X[0],L=X[1],T=Object(c.useState)([]),z=Object(l.a)(T,2),D=z[0],M=z[1],V=Object(c.useState)(f),Y=Object(l.a)(V,2),q=Y[0],K=Y[1],Q=Object(c.useState)(h),W=Object(l.a)(Q,2),Z=W[0],$=W[1],ee=Object(c.useState)(""),ae=Object(l.a)(ee,2),te=ae[0],le=ae[1],ce=Object(c.useState)(""),re=Object(l.a)(ce,2),ne=re[0],se=re[1],oe=Object(c.useState)("admin"),me=Object(l.a)(oe,2),ie=me[0],de=me[1],ue=Object(c.useState)("admin123"),pe=Object(l.a)(ue,2),Ee=pe[0],fe=pe[1],ve=Object(c.useState)("1-8"),he=Object(l.a)(ve,2),Ne=he[0],be=he[1],ge=Object(c.useState)(""),Ce=Object(l.a)(ge,2),je=Ce[0],Oe=Ce[1],ye=Object(c.useState)(""),we=Object(l.a)(ye,2),_e=we[0],Se=we[1],Ie=Object(c.useState)(""),Pe=Object(l.a)(Ie,2),xe=Pe[0],Ge=Pe[1],ke=Object(c.useState)(0),Fe=Object(l.a)(ke,2),Ue=Fe[0],Re=Fe[1],Be=Object(c.useState)(!1),He=Object(l.a)(Be,2),Ae=He[0],Xe=He[1],Je=Object(c.useState)(""),Le=Object(l.a)(Je,2),Te=Le[0],ze=Le[1],De=Object(c.useState)(""),Me=Object(l.a)(De,2),Ve=Me[0],Ye=Me[1],qe=Object(c.useState)(""),Ke=Object(l.a)(qe,2),Qe=Ke[0],We=Ke[1],Ze=Object(c.useState)(""),$e=Object(l.a)(Ze,2),ea=$e[0],aa=$e[1],ta=Object(c.useState)(""),la=Object(l.a)(ta,2),ca=la[0],ra=la[1],na=Object(c.useState)(h),sa=Object(l.a)(na,2),oa=sa[0],ma=sa[1],ia=Object(c.useState)(1),da=Object(l.a)(ia,2),ua=da[0],pa=da[1],Ea=function(){return s(!1)},fa=function(){return C(!1)},va=function(){d.a.get("v1/scene-config/cameras").then((function(e){var a=e.data;a.is_succeed&&M(a.data.channels)})).catch((function(e){console.log(e)}))},ha=function(e){K(parseInt(e.target.value))};return Object(c.useEffect)((function(){i.a.init(),d.a.get("v1/scene-config/scene").then((function(e){var a=e.data;a.is_succeed&&(w(a.data.scene_name),F(a.data.scene_address),H(a.data.gps_coordinate),L(a.data.tel_number),P(a.data.frp_port))})).catch((function(e){console.log(e)}))}),[]),Object(c.useEffect)((function(){i.a.init(),va()}),[]),r.a.createElement(r.a.Fragment,null,r.a.createElement("div",{style:{display:"flex",alignItems:"center",justifyContent:"center"}},r.a.createElement(u.a,{onClose:function(){return Xe(!1)},style:{position:"fixed",zIndex:3,width:"80%"},show:Ae,delay:5e5,autohide:!0},r.a.createElement(u.a.Header,null,r.a.createElement("strong",{className:"mr-auto"},"\u7cfb\u7edf\u914d\u7f6e"),r.a.createElement("small",null,"1 mins ago")),r.a.createElement(u.a.Body,null,Te))),r.a.createElement("div",null,r.a.createElement("div",{className:"page-header"},r.a.createElement("h3",{className:"page-title"},"\u573a\u5730\u914d\u7f6e")),r.a.createElement("div",{className:"row"},r.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},r.a.createElement("div",{className:"card"},r.a.createElement("div",{className:"card-body"},r.a.createElement("h4",{className:"card-title"},r.a.createElement("i",{className:"mdi mdi-map-marker-multiple"}),"\u573a\u5730"),r.a.createElement("form",{className:"forms-sample"},r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"sceneName",className:"col-sm-3 col-form-label"},"\u573a\u5730\u540d\u79f0"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"sceneName",placeholder:"\u573a\u5730\u540d\u79f0, \u5982\uff1a XXX\u4e2d\u5b66\u9ad8\u4e8c\u4e09\u73ed",value:y,onChange:function(e){w(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"frpPort",className:"col-sm-3 col-form-label"},"\u7aef\u53e3"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"frpPort",placeholder:"\u8fdc\u7a0b\u914d\u7f6e\u7aef\u53e3\uff0c\u5982\uff1a 23280",value:I,onChange:function(e){P(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"sceneAddress",className:"col-sm-3 col-form-label"},"\u5730\u5740"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"sceneAddress",placeholder:"\u5730\u5740",value:k,onChange:function(e){F(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"gpsCoordinate",className:"col-sm-3 col-form-label"},"GPS\u5750\u6807"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",value:B,className:"form-control",id:"gpsCoordinate",onChange:function(e){H(e.target.value)},placeholder:"\u5982\uff1a 2450.334, 3351.34"}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"telephone",className:"col-sm-3 col-form-label"},"\u8054\u7cfb\u7535\u8bdd"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",value:J,className:"form-control",id:"telephone",onChange:function(e){L(e.target.value)},placeholder:"\u5ea7\u673a\u6216\u624b\u673a\u53f7\u7801\uff0c\u5982\uff1a 0755-28964567, 13954324569"}))),r.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){var e={name:y,address:k,port:I,tel_number:J,gps_coordinate:B};d.a.post("v1/scene-config/scene",e).then((function(e){var a=e.data;a.is_succeed?(ze("\u66f4\u65b0\u573a\u5730\u6210\u529f\uff01"),Xe(!0)):(console.log("\u66f4\u65b0\u573a\u5730\u5931\u8d25: ".concat(a.message)),ze("\u66f4\u65b0\u573a\u5730\u5931\u8d25\uff01"),Xe(!0))})).catch((function(e){console.log("\u66f4\u65b0\u573a\u5730\u5931\u8d25: ".concat(e.message)),ze("\u66f4\u65b0\u573a\u5730\u5931\u8d25\uff01"),Xe(!0)}))}},"\u786e\u5b9a"))))),r.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},r.a.createElement("div",{className:"card"},r.a.createElement("div",{className:"card-body"},r.a.createElement("h4",{className:"card-title"},r.a.createElement("i",{className:"mdi mdi-video"}),"\u89c6\u9891\u914d\u7f6e"),r.a.createElement("p",{className:"card-description"},"\u6ce8\uff1a \u901a\u8fc7\u5f55\u50cf\u673a\u53ef\u4ee5\u4e00\u6b21\u6027\u6dfb\u52a0\u591a\u4e2a\u901a\u9053\uff0c\u4f46\u901a\u8fc7\u6444\u50cf\u5934\u6dfb\u52a0\u65f6\u9700\u4e00\u4e2a\u4e00\u4e2a\u5355\u72ec\u6dfb\u52a0\uff0c\u56e0\u4e3a\u6bcf\u4e2a\u6444\u50cf\u5934IP\u90fd\u4e0d\u4e00\u6837"),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{className:"col-sm-3 col-form-label"},"\u53d6\u6d41\u65b9\u5f0f"),r.a.createElement("div",{className:"col-sm-4"},r.a.createElement("div",{className:"form-check"},r.a.createElement("label",{className:"form-check-label"},r.a.createElement("input",{type:"radio",className:"form-check-input",name:"rtspSourceRecorder",id:"rtspSourceRecorder",value:f,onChange:ha,checked:q===f})," \u901a\u8fc7\u5f55\u50cf\u673a",r.a.createElement("i",{className:"input-helper"})))),r.a.createElement("div",{className:"col-sm-5"},r.a.createElement("div",{className:"form-check"},r.a.createElement("label",{className:"form-check-label"},r.a.createElement("input",{type:"radio",className:"form-check-input",name:"rtspSourceCamera",id:"rtspSourceCamera",value:v,onChange:ha,checked:q===v})," \u901a\u8fc7\u6444\u50cf\u5934",r.a.createElement("i",{className:"input-helper"}))))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{className:"col-sm-3 col-form-label"},"\u5f55\u50cf\u673a\u54c1\u724c"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement("select",{className:"form-control",onChange:function(e){$(parseInt(e.target.value))}},r.a.createElement("option",{value:h,selected:Z===h},"\u6d77\u5eb7\u5a01\u89c6"),r.a.createElement("option",{value:N,selected:Z===N},"\u5927\u534e")))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"channelName",className:"col-sm-3 col-form-label"},"\u901a\u9053\u540d\u79f0"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"channelName",onChange:function(e){le(e.target.value)},placeholder:"\u5982\u679c\u662f\u901a\u8fc7\u5f55\u50cf\u673a\u6dfb\u52a0\uff0c\u5219\u5728\u8fd9\u91cc\u53ef\u4ee5\u8f93\u5165\u591a\u4e2a\u901a\u9053\u540d\u79f0\uff0c\u4ee5\u9017\u53f7\u9694\u5f00\uff0c\u4e0e\u540e\u9762\u6279\u91cf\u6dfb\u52a0\u901a\u9053\u5bf9\u5e94\uff01",value:te}))),q===f?r.a.createElement("div",{className:"forms-sample"},r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"videoRecorderIP",className:"col-sm-3 col-form-label"},"\u5f55\u50cf\u673aIP"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"videoRecorderIP",placeholder:"\u5f55\u50cf\u673aIP",value:ne,onChange:function(e){se(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"rtspUserName",className:"col-sm-3 col-form-label"},"\u7528\u6237\u540d"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"rtspUserName",onChange:function(e){de(e.target.value)},placeholder:"\u7528\u6237\u540d",value:ie}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"rtspPassword",className:"col-sm-3 col-form-label"},"\u5bc6\u7801"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"rtspPassword",onChange:function(e){fe(e.target.value)},placeholder:"\u5bc6\u7801",value:Ee}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"rtspChannels",className:"col-sm-3 col-form-label"},"\u901a\u9053"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"rtspChannels",placeholder:"\u652f\u6301\u9017\u53f7\u9694\u5f00(1,3,5)\u548c\u8303\u56f4\u6307\u5b9a(1-8)\u4e24\u79cd\u683c\u5f0f",value:Ne,onChange:function(e){be(e.target.value)}})))):r.a.createElement("div",{className:"forms-sample"},r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"cameraIP",className:"col-sm-3 col-form-label"},"\u6444\u50cf\u5934IP"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"cameraIP",placeholder:"\u6444\u50cf\u5934IP",value:je,onChange:function(e){Oe(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"cameraUserName",className:"col-sm-3 col-form-label"},"\u7528\u6237\u540d"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"cameraUserName",placeholder:"\u7528\u6237\u540d",value:_e,onChange:function(e){Se(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"cameraPassword",className:"col-sm-3 col-form-label"},"\u5bc6\u7801"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"cameraPassword",placeholder:"\u5bc6\u7801",value:xe,onChange:function(e){Ge(e.target.value)}})))),r.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){var e=[];if(q===f){if(""===Ne)return void alert("\u8bf7\u8f93\u5165\u901a\u9053\u53f7\uff01");if(""===ie||""===Ee)return void alert("\u8bf7\u8f93\u5165\u5f55\u50cf\u673a\u7528\u6237\u540d\u548c\u5bc6\u7801\uff01");if(""===ne)return void alert("\u8bf7\u8f93\u5165\u5f55\u50cf\u673aIP\uff01");for(var a=te.split(","),t=0,l=Ne.split(","),c=0;c<l.length;c++){var r=l[c];if(r.includes("-")){var n=r.split("-");if(2==n.length&&n[0]<n[1])for(var s=parseInt(n[0]);s<=parseInt(n[1]);s++){var o={name:t>=0&&t<a.length?a[t]:"\u672a\u547d\u540d\u901a\u9053",camera_vendor:Z,rtsp_user:ie,rtsp_password:Ee,rtsp_ip:ne,rtsp_channel_id:s};e.push(o)}}else{var m={name:t>=0&&t<a.length?a[t]:"\u672a\u547d\u540d\u901a\u9053",camera_vendor:Z,rtsp_user:ie,rtsp_password:Ee,rtsp_ip:ne,rtsp_channel_id:parseInt(r)};e.push(m)}t++}}else{if(""===je)return void alert("\u8bf7\u8f93\u5165\u6444\u50cf\u5934IP\uff01");if(""===_e||""===xe)return void alert("\u8bf7\u8f93\u5165\u6444\u50cf\u5934\u7528\u6237\u540d\u548c\u5bc6\u7801\uff01");var i={name:te,camera_vendor:Z,rtsp_user:_e,rtsp_password:xe,rtsp_ip:je,rtsp_channel_id:1};e.push(i)}for(var u=[],p=0;p<e.length;p++){var E=d.a.post("v1/scene-config/cameras",e[p]);u.push(E)}Promise.all(u).then((function(e){console.log(e);for(var a=!0,t="",l=0;l<e.length;l++)e[l].data.is_succeed||(a=!1,t=t+","+e[l].data.message);a?(ze("\u6dfb\u52a0\u6444\u50cf\u5934\u901a\u9053\u6210\u529f\uff01"),Xe(!0),va()):(console.log("\u6dfb\u52a0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25: ".concat(t)),ze("\u6dfb\u52a0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25\uff01"),Xe(!0))})).catch((function(e){console.log("\u6dfb\u52a0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25: ".concat(e.message)),ze("\u6dfb\u52a0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25\uff01"),Xe(!0)}))}},"\u6dfb\u52a0")))),r.a.createElement("div",{className:"col-lg-12 grid-margin stretch-card"},r.a.createElement("div",{className:"card"},r.a.createElement("div",{className:"card-body"},r.a.createElement("h4",{className:"card-title"},"\u901a\u9053\u5217\u8868"),r.a.createElement("p",{className:"card-description"},"\u5df2\u6dfb\u52a0\u6444\u50cf\u5934\u901a\u9053\u4e8e\u4ee5\u4e0b\u5217\u8868\u663e\u793a"),r.a.createElement("div",{className:"table-responsive"},r.a.createElement("table",{className:"table table-striped"},r.a.createElement("thead",null,r.a.createElement("tr",null,r.a.createElement("th",null," \u7f16\u53f7 "),r.a.createElement("th",null," \u540d\u79f0 "),r.a.createElement("th",null," IP "),r.a.createElement("th",null," \u5f55\u50cf\u673a\u54c1\u724c "),r.a.createElement("th",null," \u7528\u6237\u540d "),r.a.createElement("th",null," \u5bc6\u7801 "),r.a.createElement("th",null," \u64cd\u4f5c "))),r.a.createElement("tbody",null,D.length>0?D.map((function(e,a){return r.a.createElement("tr",{key:"ch-".concat(e.id)},r.a.createElement("td",{className:"py-1"},e.id),r.a.createElement("td",null," ",e.name," "),r.a.createElement("td",null," ",e.rtsp_ip," "),r.a.createElement("td",null," ",e.camera_vendor==h?"\u6d77\u5eb7":"\u5927\u534e"," "),r.a.createElement("td",null," ",e.rtsp_user," "),r.a.createElement("td",null," ",e.rtsp_password," "),r.a.createElement("td",null,r.a.createElement("div",{style:{display:"flex",alignItems:"center",justifyContent:"start"}},r.a.createElement("div",{className:"mr-3",onClick:function(){Re(a),s(!0)},style:{cursor:"pointer"}},r.a.createElement("i",{className:"mdi mdi-delete icon-sm text-primary align-middle"})),r.a.createElement("div",{className:"mx-3",onClick:function(){Re(a),Ye(e.name),We(e.rtsp_ip),ma(e.camera_vendor),pa(e.rtsp_channel_id),aa(e.rtsp_user),ra(e.rtsp_password),C(!0)},style:{cursor:"pointer"}},r.a.createElement("i",{className:"mdi mdi-settings icon-sm text-primary align-middle"})))))})):r.a.createElement("tr",null,r.a.createElement("td",null,"'\u6ca1\u6709\u901a\u9053\u53ef\u663e\u793a\uff01'")))))))))),r.a.createElement(p.a,{show:t,onHide:Ea},r.a.createElement(p.a.Header,{closeButton:!0},r.a.createElement(p.a.Title,null,"\u8b66\u544a")),r.a.createElement(p.a.Body,null,D.length>0&&Ue>=0&&Ue<D.length?"\u5373\u5c06\u5220\u9664\u901a\u9053\uff1a".concat(D[Ue].name,"\uff0c\u662f\u5426\u7ee7\u7eed"):""),r.a.createElement(p.a.Footer,null,r.a.createElement(E.a,{variant:"secondary",onClick:Ea},"\u53d6\u6d88"),r.a.createElement(E.a,{variant:"primary",onClick:function(){!function(e){var a=D[e].name;Ea(),d.a.delete("v1/scene-config/cameras/".concat(D[e].id)).then((function(e){var t=e.data;t.is_succeed?(ze("\u5220\u9664\u901a\u9053 '".concat(a,"' \u6210\u529f\uff01")),Xe(!0),va()):(console.log("\u5220\u9664\u901a\u9053 '".concat(a,"' \u5931\u8d25: ")+t.message),ze("\u5220\u9664\u901a\u9053 '".concat(a,"' \u5931\u8d25\uff01")),Xe(!0))})).catch((function(e){console.log("\u5220\u9664\u901a\u9053 '".concat(a,"' \u5931\u8d25: ")+e.message),ze("\u5220\u9664\u901a\u9053 '".concat(a,"' \u5931\u8d25\uff01")),Xe(!0)}))}(Ue)}},"\u786e\u5b9a"))),r.a.createElement(p.a,{show:g,onHide:fa},r.a.createElement(p.a.Header,{closeButton:!0},r.a.createElement(p.a.Title,null,"\u901a\u9053\u7f16\u8f91")),r.a.createElement(p.a.Body,{style:{height:"465px",overflowY:"scroll"}},r.a.createElement("div",{className:"col-md-12 grid-margin stretch-card"},r.a.createElement("div",{className:"card"},r.a.createElement("div",{className:"card-body"},r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{className:"col-sm-3 col-form-label"},"\u5f55\u50cf\u673a\u54c1\u724c"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement("select",{className:"form-control",onChange:function(e){ma(parseInt(e.target.value))}},r.a.createElement("option",{value:h,selected:oa===h},"\u6d77\u5eb7\u5a01\u89c6"),r.a.createElement("option",{value:N,selected:oa===N},"\u5927\u534e")))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"editCameraChannelName",className:"col-sm-3 col-form-label"},"\u901a\u9053\u540d\u79f0"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"editCameraChannelName",placeholder:"\u901a\u9053\u540d\u79f0",value:Ve,onChange:function(e){Ye(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"editCameraIP",className:"col-sm-3 col-form-label"},"\u6444\u50cf\u5934IP"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"editCameraIP",placeholder:"\u6444\u50cf\u5934IP",value:Qe,onChange:function(e){We(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"editCameraUserName",className:"col-sm-3 col-form-label"},"\u7528\u6237\u540d"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"editCameraUserName",placeholder:"\u7528\u6237\u540d",value:ea,onChange:function(e){aa(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"editCameraPassword",className:"col-sm-3 col-form-label"},"\u5bc6\u7801"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"editCameraPassword",placeholder:"\u5bc6\u7801",value:ca,onChange:function(e){ra(e.target.value)}}))),r.a.createElement(o.a.Group,{className:"row"},r.a.createElement("label",{htmlFor:"editCameraChannelId",className:"col-sm-3 col-form-label"},"\u901a\u9053ID"),r.a.createElement("div",{className:"col-sm-9"},r.a.createElement(o.a.Control,{type:"number",className:"form-control",id:"editCameraChannelId",placeholder:"\u5bc6\u7801",value:ua,onChange:function(e){pa(parseInt(e.target.value))}}))))))),r.a.createElement(p.a.Footer,null,r.a.createElement(E.a,{variant:"secondary",onClick:fa},"\u53d6\u6d88"),r.a.createElement(E.a,{variant:"primary",onClick:function(){!function(e){fa();var a={name:Ve,camera_vendor:oa,rtsp_user:ea,rtsp_password:ca,rtsp_ip:Qe,rtsp_channel_id:ua};d.a.put("v1/scene-config/cameras/".concat(D[e].id),a).then((function(e){var a=e.data;a.is_succeed?(ze("\u66f4\u65b0\u6444\u50cf\u5934\u901a\u9053\u6210\u529f\uff01"),Xe(!0),va()):(console.log("\u66f4\u65b0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25: ".concat(a.message)),ze("\u66f4\u65b0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25\uff01"),Xe(!0))})).catch((function(e){console.log("\u66f4\u65b0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25: ".concat(e.message)),ze("\u66f4\u65b0\u6444\u50cf\u5934\u901a\u9053\u5931\u8d25\uff01"),Xe(!0)}))}(Ue)}},"\u786e\u5b9a"))))}}}]);
//# sourceMappingURL=11.f1a44c01.chunk.js.map