(window["webpackJsonpls-host-config"]=window["webpackJsonpls-host-config"]||[]).push([[12],{120:function(e,a,t){"use strict";var c=t(127),l=t.n(c).a.create({baseURL:"/api/",timeout:1e4,headers:{"ls-token":"1234567890abcdef"}});a.a=l},124:function(e,a,t){"use strict";t.d(a,"a",(function(){return c}));var c=function(){return([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,(function(e){return(e^crypto.getRandomValues(new Uint8Array(1))[0]&15>>e/4).toString(16)}))}},298:function(e,a,t){"use strict";t.r(a),t.d(a,"default",(function(){return u}));var c=t(52),l=t(0),o=t.n(l),s=(t(4),t(39)),n=t(152),r=t(126),m=t.n(r),i=t(120),d=t(153);t(124);Object(s.a)();function u(){var e=Object(l.useState)(""),a=Object(c.a)(e,2),t=a[0],s=a[1],r=Object(l.useState)(""),u=Object(c.a)(r,2),h=u[0],f=u[1],b=Object(l.useState)(""),g=Object(c.a)(b,2),E=g[0],N=g[1],p=Object(l.useState)(""),v=Object(c.a)(p,2),y=(v[0],v[1],Object(l.useState)("")),j=Object(c.a)(y,2),O=(j[0],j[1],Object(l.useState)("")),w=Object(c.a)(O,2),C=w[0],S=w[1],_=Object(l.useState)(24),x=Object(c.a)(_,2),k=x[0],I=x[1],F=Object(l.useState)(""),G=Object(c.a)(F,2),H=G[0],K=G[1],P=Object(l.useState)("255.255.255.0"),R=Object(c.a)(P,2),L=R[0],z=R[1],D=Object(l.useState)("114.114.114.114,8.8.8.8"),J=Object(c.a)(D,2),T=J[0],U=J[1],A=Object(l.useState)(""),B=Object(c.a)(A,2),M=B[0],V=B[1],Y=Object(l.useState)(""),q=Object(c.a)(Y,2),Q=q[0],W=q[1],X=Object(l.useState)(!1),Z=Object(c.a)(X,2),$=Z[0],ee=Z[1],ae=Object(l.useState)(""),te=Object(c.a)(ae,2),ce=te[0],le=te[1];return Object(l.useEffect)((function(){m.a.init(),i.a.get("v1/system-config/host").then((function(e){var a=e.data;a.is_succeed&&(s(a.data.host_name),f(a.data.host_id),N(a.data.host_key),I(a.data.auto_reboot_interval_hours))})).catch((function(e){console.log(e)}))}),[]),Object(l.useEffect)((function(){m.a.init(),i.a.get("v1/system-config/network").then((function(e){var a=e.data;a.is_succeed&&(S(a.data.host_ip),z(a.data.mask),K(a.data.default_gateway),U(a.data.dns))})).catch((function(e){console.log(e)}))}),[]),o.a.createElement(o.a.Fragment,null,o.a.createElement("div",{style:{display:"flex",alignItems:"center",justifyContent:"center"}},o.a.createElement(d.a,{onClose:function(){return ee(!1)},style:{position:"fixed",zIndex:3,width:"80%"},show:$,delay:5e5,autohide:!0},o.a.createElement(d.a.Header,null,o.a.createElement("strong",{className:"mr-auto"},"\u7cfb\u7edf\u914d\u7f6e"),o.a.createElement("small",null,"1 mins ago")),o.a.createElement(d.a.Body,null,ce))),o.a.createElement("div",null,o.a.createElement("div",{className:"page-header"},o.a.createElement("h3",{className:"page-title"},"\u7cfb\u7edf\u8bbe\u7f6e")),o.a.createElement("div",{className:"row"},o.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},o.a.createElement("div",{className:"card"},o.a.createElement("div",{className:"card-body"},o.a.createElement("h4",{className:"card-title"},o.a.createElement("i",{className:"mdi mdi-laptop"}),"\u4e3b\u673a\u4fe1\u606f"),o.a.createElement("form",{className:"forms-sample"},o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"hostName",className:"col-sm-3 col-form-label"},"\u4e3b\u673a\u540d"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",className:"form-control",id:"hostName",placeholder:"\u4e3b\u673a\u540d\uff0c \u5982\uff1a ls-host-23280",value:t,onChange:function(e){s(e.target.value)}}))),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"hostId",className:"col-sm-3 col-form-label"},"Host Id"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",className:"form-control",id:"hostId",onChange:function(e){f(e.target.value)},placeholder:"Host Id",value:h}))),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"hostKey",className:"col-sm-3 col-form-label"},"Host Key"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",className:"form-control",id:"hostKey",onChange:function(e){N(e.target.value)},placeholder:"Host Key",value:E}))),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"systemRebootIntervalHour",className:"col-sm-3 col-form-label"},"\u5b9a\u65f6\u91cd\u542f\uff08\u5c0f\u65f6\uff09"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"number",className:"form-control",id:"systemRebootIntervalHour",value:k,onChange:function(e){I(parseInt(e.target.value))},placeholder:"\u8bbe\u7f6e\u81ea\u52a8\u91cd\u542f\u65f6\u95f4\u95f4\u9694"}))),o.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){var e={host_name:t,host_id:h,host_key:E,system_reboot_interval_hours:k};i.a.post("v1/system-config/host",e).then((function(e){var a=e.data;a.is_succeed?(le("\u66f4\u65b0\u4e3b\u673a\u914d\u7f6e\u6210\u529f\uff01"),ee(!0)):(console.log("\u66f4\u65b0\u4e3b\u673a\u914d\u7f6e\u5931\u8d25: ".concat(a.message)),le("\u66f4\u65b0\u4e3b\u673a\u914d\u7f6e\u5931\u8d25\uff01"),ee(!0))})).catch((function(e){console.log("\u66f4\u65b0\u4e3b\u673a\u914d\u7f6e\u5931\u8d25: ".concat(e.message)),le("\u66f4\u65b0\u4e3b\u673a\u914d\u7f6e\u5931\u8d25\uff01"),ee(!0)}))}},"\u786e\u5b9a"))))),o.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},o.a.createElement("div",{className:"card"},o.a.createElement("div",{className:"card-body"},o.a.createElement("h4",{className:"card-title"},o.a.createElement("i",{className:"mdi mdi-ethernet"}),"\u7f51\u7edc\u914d\u7f6e"),o.a.createElement("form",{className:"forms-sample"},o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"hostIP",className:"col-sm-3 col-form-label"},"IP"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",className:"form-control",id:"hostIP",placeholder:"IP\u5730\u5740, \u5982\uff1a 192.168.2.100",value:C,onChange:function(e){S(e.target.value)}}))),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"defaultGateway",className:"col-sm-3 col-form-label"},"\u9ed8\u8ba4\u7f51\u5173"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",className:"form-control",id:"defaultGateway",placeholder:"\u9ed8\u8ba4\u7f51\u5173\uff0c\u5982\uff1a 192.168.2.1",value:H,onChange:function(e){K(e.target.value)}}))),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"mask",className:"col-sm-3 col-form-label"},"\u5b50\u7f51\u63a9\u7801"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",className:"form-control",id:"mask",placeholder:"\u5b50\u7f51\u63a9\u7801\uff0c\u5982\uff1a 255.255.255.0",value:L,onChange:function(e){z(e.target.value)}}))),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"dns",className:"col-sm-3 col-form-label"},"DNS(\u9017\u53f7\u9694\u5f00)"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",value:T,className:"form-control",id:"dns",onChange:function(e){U(e.target.value)},placeholder:"DNS, \u5982\uff1a 114.114.114.114,8.8.8.8"}))),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("button",{type:"button",className:"btn btn-gradient-primary col-sm-6 col-md-3 col-lg-3 mt-2",onClick:function(){if(""!==C&&""!==H){var e={method:"static",ip:C,mask:L,dns:T,gateway:H};i.a.post("v1/system-config/network",e).then((function(e){var a=e.data;a.is_succeed?(le("\u914d\u7f6e\u7f51\u7edc\u6210\u529f\uff01"),ee(!0)):(console.log("\u914d\u7f6e\u7f51\u7edc\u5931\u8d25: ".concat(a.message)),le("\u914d\u7f6e\u7f51\u7edc\u5931\u8d25\uff01"),ee(!0))})).catch((function(e){console.log("\u914d\u7f6e\u7f51\u7edc\u5931\u8d25: ".concat(e.message)),le("\u914d\u7f6e\u7f51\u7edc\u5931\u8d25\uff01"),ee(!0)}))}else alert("\u8bf7\u8f93\u5165\u8981\u914d\u7684IP\u548c\u7f51\u5173\uff01")}},"\u786e\u5b9a"),o.a.createElement("button",{type:"button",className:"btn btn-gradient-danger col-sm-6 col-md-3 col-lg-3 mt-2",onClick:function(){i.a.post("v1/system-config/network",{method:"dhcp"}).then((function(e){var a=e.data;a.is_succeed?(le("\u91cd\u7f6e\u7f51\u7edc\u6210\u529f\uff01"),ee(!0)):(console.log("\u91cd\u7f6e\u7f51\u7edc\u5931\u8d25: ".concat(a.message)),le("\u91cd\u7f6e\u7f51\u7edc\u5931\u8d25\uff01"),ee(!0))})).catch((function(e){console.log("\u91cd\u7f6e\u7f51\u7edc\u5931\u8d25: ".concat(e.message)),le("\u91cd\u7f6e\u7f51\u7edc\u5931\u8d25\uff01"),ee(!0)}))}},"\u91cd\u7f6e")))))),o.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},o.a.createElement("div",{className:"card"},o.a.createElement("div",{className:"card-body"},o.a.createElement("h4",{className:"card-title"},o.a.createElement("i",{className:"mdi mdi-video"}),"\u6267\u884cShell\u547d\u4ee4"),o.a.createElement("p",{className:"card-description"},"\u6ce8\uff1a \u8f93\u5165\u6846\u4e2d\u8f93\u5165Linux Shell\u547d\u4ee4\uff0c \u70b9\u51fb\u786e\u8ba4\u53d1\u9001\u547d\u4ee4\u6267\u884c\uff0c \u6267\u884c\u7ed3\u679c\u5c06\u4e8e\u4e0b\u9762\u65b9\u6846\u533a\u663e\u793a"),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("label",{htmlFor:"shellCmd",className:"col-sm-3 col-form-label"},"\u547d\u4ee4"),o.a.createElement("div",{className:"col-sm-9"},o.a.createElement(n.a.Control,{type:"text",className:"form-control",id:"shellCmd",value:M,onChange:function(e){V(e.target.value)},placeholder:"\u8f93\u5165Linux Shell\u547d\u4ee4, \u5982ps aux | grep TKTMesh"}))),o.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){if(""!==M){var e={cmd:M};i.a.post("v1/system-config/shell-cmd",e).then((function(e){var a=e.data;a.is_succeed?(console.log("Cmd result:",a.data),W(a.data.cmd_result)):(console.log("\u6267\u884c\u547d\u4ee4\u5931\u8d25: ".concat(a.message)),W("\u6267\u884c\u547d\u4ee4\u5931\u8d25: ".concat(a.message)))})).catch((function(e){console.log("\u6267\u884c\u547d\u4ee4\u5931\u8d25: ".concat(e.message)),W("\u6267\u884c\u547d\u4ee4\u5931\u8d25: ".concat(e.message))}))}}},"\u6267\u884c"),o.a.createElement(n.a.Group,{className:"row"},o.a.createElement("div",{className:"mt-4"},"\u547d\u4ee4\u6267\u884c\u7ed3\u679c:"),o.a.createElement("textarea",{cols:"90",value:Q,maxLength:"999999",id:"cmdResult",className:"col-sm-12",style:{border:"dashed 1px #CFCFCF",resize:"both",height:"280px",overflowY:"scroll",width:"100%",fontSize:"12px"}}))))))))}}}]);
//# sourceMappingURL=12.07508f7a.chunk.js.map