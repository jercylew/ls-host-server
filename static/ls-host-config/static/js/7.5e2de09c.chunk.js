(window["webpackJsonpls-host-config"]=window["webpackJsonpls-host-config"]||[]).push([[7],{119:function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),a.default=function(){for(var e=arguments.length,a=Array(e),t=0;t<e;t++)a[t]=arguments[t];function l(){for(var e=arguments.length,t=Array(e),l=0;l<e;l++)t[l]=arguments[l];var r=null;return a.forEach((function(e){if(null==r){var a=e.apply(void 0,t);null!=a&&(r=a)}})),r}return(0,c.default)(l)};var l,r=t(126),c=(l=r)&&l.__esModule?l:{default:l};e.exports=a.default},121:function(e,a,t){"use strict";var l=t(128),r=t.n(l).a.create({baseURL:"http://localhost/api/",timeout:1e4,headers:{"ls-token":"1234567890abcdef"}});a.a=r},124:function(e,a,t){"use strict";t.d(a,"a",(function(){return l}));var l=function(){return([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,(function(e){return(e^crypto.getRandomValues(new Uint8Array(1))[0]&15>>e/4).toString(16)}))}},126:function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),a.default=function(e){function a(a,t,l,r,c,s){var o=r||"<<anonymous>>",n=s||l;if(null==t[l])return a?new Error("Required "+c+" `"+n+"` was not specified in `"+o+"`."):null;for(var m=arguments.length,i=Array(m>6?m-6:0),d=6;d<m;d++)i[d-6]=arguments[d];return e.apply(void 0,[t,l,o,c,n].concat(i))}var t=a.bind(null,!1);return t.isRequired=a.bind(null,!0),t},e.exports=a.default},138:function(e,a,t){"use strict";var l=t(1),r=t(2),c=t(7),s=t.n(c),o=t(0),n=t.n(o),m=(t(119),t(3)),i=t.n(m),d=["as","className","type","tooltip"],u={type:i.a.string,tooltip:i.a.bool,as:i.a.elementType},f=n.a.forwardRef((function(e,a){var t=e.as,c=void 0===t?"div":t,o=e.className,m=e.type,i=void 0===m?"valid":m,u=e.tooltip,f=void 0!==u&&u,b=Object(r.a)(e,d);return n.a.createElement(c,Object(l.a)({},b,{ref:a,className:s()(o,i+"-"+(f?"tooltip":"feedback"))}))}));f.displayName="Feedback",f.propTypes=u;var b=f,v=n.a.createContext({controlId:void 0}),p=t(8),N=["id","bsPrefix","bsCustomPrefix","className","type","isValid","isInvalid","isStatic","as"],h=n.a.forwardRef((function(e,a){var t=e.id,c=e.bsPrefix,m=e.bsCustomPrefix,i=e.className,d=e.type,u=void 0===d?"checkbox":d,f=e.isValid,b=void 0!==f&&f,h=e.isInvalid,E=void 0!==h&&h,y=e.isStatic,O=e.as,j=void 0===O?"input":O,g=Object(r.a)(e,N),x=Object(o.useContext)(v),C=x.controlId,w=x.custom?[m,"custom-control-input"]:[c,"form-check-input"],P=w[0],k=w[1];return c=Object(p.a)(P,k),n.a.createElement(j,Object(l.a)({},g,{ref:a,type:u,id:t||C,className:s()(i,c,b&&"is-valid",E&&"is-invalid",y&&"position-static")}))}));h.displayName="FormCheckInput";var E=h,y=["bsPrefix","bsCustomPrefix","className","htmlFor"],O=n.a.forwardRef((function(e,a){var t=e.bsPrefix,c=e.bsCustomPrefix,m=e.className,i=e.htmlFor,d=Object(r.a)(e,y),u=Object(o.useContext)(v),f=u.controlId,b=u.custom?[c,"custom-control-label"]:[t,"form-check-label"],N=b[0],h=b[1];return t=Object(p.a)(N,h),n.a.createElement("label",Object(l.a)({},d,{ref:a,htmlFor:i||f,className:s()(m,t)}))}));O.displayName="FormCheckLabel";var j=O,g=["id","bsPrefix","bsCustomPrefix","inline","disabled","isValid","isInvalid","feedbackTooltip","feedback","className","style","title","type","label","children","custom","as"],x=n.a.forwardRef((function(e,a){var t=e.id,c=e.bsPrefix,m=e.bsCustomPrefix,i=e.inline,d=void 0!==i&&i,u=e.disabled,f=void 0!==u&&u,N=e.isValid,h=void 0!==N&&N,y=e.isInvalid,O=void 0!==y&&y,x=e.feedbackTooltip,C=void 0!==x&&x,w=e.feedback,P=e.className,k=e.style,F=e.title,I=void 0===F?"":F,S=e.type,T=void 0===S?"checkbox":S,R=e.label,M=e.children,G=e.custom,L=e.as,V=void 0===L?"input":L,q=Object(r.a)(e,g),A="switch"===T||G,D=A?[m,"custom-control"]:[c,"form-check"],Q=D[0],_=D[1];c=Object(p.a)(Q,_);var z=Object(o.useContext)(v).controlId,K=Object(o.useMemo)((function(){return{controlId:t||z,custom:A}}),[z,A,t]),U=A||null!=R&&!1!==R&&!M,J=n.a.createElement(E,Object(l.a)({},q,{type:"switch"===T?"checkbox":T,ref:a,isValid:h,isInvalid:O,isStatic:!U,disabled:f,as:V}));return n.a.createElement(v.Provider,{value:K},n.a.createElement("div",{style:k,className:s()(P,c,A&&"custom-"+T,d&&c+"-inline")},M||n.a.createElement(n.a.Fragment,null,J,U&&n.a.createElement(j,{title:I},R),(h||O)&&n.a.createElement(b,{type:h?"valid":"invalid",tooltip:C},w))))}));x.displayName="FormCheck",x.Input=E,x.Label=j;var C=x,w=["id","bsPrefix","bsCustomPrefix","className","isValid","isInvalid","lang","as"],P=n.a.forwardRef((function(e,a){var t=e.id,c=e.bsPrefix,m=e.bsCustomPrefix,i=e.className,d=e.isValid,u=e.isInvalid,f=e.lang,b=e.as,N=void 0===b?"input":b,h=Object(r.a)(e,w),E=Object(o.useContext)(v),y=E.controlId,O=E.custom?[m,"custom-file-input"]:[c,"form-control-file"],j=O[0],g=O[1];return c=Object(p.a)(j,g),n.a.createElement(N,Object(l.a)({},h,{ref:a,id:t||y,type:"file",lang:f,className:s()(i,c,d&&"is-valid",u&&"is-invalid")}))}));P.displayName="FormFileInput";var k=P,F=["bsPrefix","bsCustomPrefix","className","htmlFor"],I=n.a.forwardRef((function(e,a){var t=e.bsPrefix,c=e.bsCustomPrefix,m=e.className,i=e.htmlFor,d=Object(r.a)(e,F),u=Object(o.useContext)(v),f=u.controlId,b=u.custom?[c,"custom-file-label"]:[t,"form-file-label"],N=b[0],h=b[1];return t=Object(p.a)(N,h),n.a.createElement("label",Object(l.a)({},d,{ref:a,htmlFor:i||f,className:s()(m,t),"data-browse":d["data-browse"]}))}));I.displayName="FormFileLabel";var S=I,T=["id","bsPrefix","bsCustomPrefix","disabled","isValid","isInvalid","feedbackTooltip","feedback","className","style","label","children","custom","lang","data-browse","as","inputAs"],R=n.a.forwardRef((function(e,a){var t=e.id,c=e.bsPrefix,m=e.bsCustomPrefix,i=e.disabled,d=void 0!==i&&i,u=e.isValid,f=void 0!==u&&u,N=e.isInvalid,h=void 0!==N&&N,E=e.feedbackTooltip,y=void 0!==E&&E,O=e.feedback,j=e.className,g=e.style,x=e.label,C=e.children,w=e.custom,P=e.lang,F=e["data-browse"],I=e.as,R=void 0===I?"div":I,M=e.inputAs,G=void 0===M?"input":M,L=Object(r.a)(e,T),V=w?[m,"custom"]:[c,"form-file"],q=V[0],A=V[1];c=Object(p.a)(q,A);var D=Object(o.useContext)(v).controlId,Q=Object(o.useMemo)((function(){return{controlId:t||D,custom:w}}),[D,w,t]),_=null!=x&&!1!==x&&!C,z=n.a.createElement(k,Object(l.a)({},L,{ref:a,isValid:f,isInvalid:h,disabled:d,as:G,lang:P}));return n.a.createElement(v.Provider,{value:Q},n.a.createElement(R,{style:g,className:s()(j,c,w&&"custom-file")},C||n.a.createElement(n.a.Fragment,null,w?n.a.createElement(n.a.Fragment,null,z,_&&n.a.createElement(S,{"data-browse":F},x)):n.a.createElement(n.a.Fragment,null,_&&n.a.createElement(S,null,x),z),(f||h)&&n.a.createElement(b,{type:f?"valid":"invalid",tooltip:y},O))))}));R.displayName="FormFile",R.Input=k,R.Label=S;var M=R,G=(t(51),["bsPrefix","bsCustomPrefix","type","size","htmlSize","id","className","isValid","isInvalid","plaintext","readOnly","custom","as"]),L=n.a.forwardRef((function(e,a){var t,c,m=e.bsPrefix,i=e.bsCustomPrefix,d=e.type,u=e.size,f=e.htmlSize,b=e.id,N=e.className,h=e.isValid,E=void 0!==h&&h,y=e.isInvalid,O=void 0!==y&&y,j=e.plaintext,g=e.readOnly,x=e.custom,C=e.as,w=void 0===C?"input":C,P=Object(r.a)(e,G),k=Object(o.useContext)(v).controlId,F=x?[i,"custom"]:[m,"form-control"],I=F[0],S=F[1];if(m=Object(p.a)(I,S),j)(c={})[m+"-plaintext"]=!0,t=c;else if("file"===d){var T;(T={})[m+"-file"]=!0,t=T}else if("range"===d){var R;(R={})[m+"-range"]=!0,t=R}else if("select"===w&&x){var M;(M={})[m+"-select"]=!0,M[m+"-select-"+u]=u,t=M}else{var L;(L={})[m]=!0,L[m+"-"+u]=u,t=L}return n.a.createElement(w,Object(l.a)({},P,{type:d,size:f,ref:a,readOnly:g,id:b||k,className:s()(N,t,E&&"is-valid",O&&"is-invalid")}))}));L.displayName="FormControl";var V=Object.assign(L,{Feedback:b}),q=["bsPrefix","className","children","controlId","as"],A=n.a.forwardRef((function(e,a){var t=e.bsPrefix,c=e.className,m=e.children,i=e.controlId,d=e.as,u=void 0===d?"div":d,f=Object(r.a)(e,q);t=Object(p.a)(t,"form-group");var b=Object(o.useMemo)((function(){return{controlId:i}}),[i]);return n.a.createElement(v.Provider,{value:b},n.a.createElement(u,Object(l.a)({},f,{ref:a,className:s()(c,t)}),m))}));A.displayName="FormGroup";var D=A,Q=["bsPrefix","className","as"],_=["xl","lg","md","sm","xs"],z=n.a.forwardRef((function(e,a){var t=e.bsPrefix,c=e.className,o=e.as,m=void 0===o?"div":o,i=Object(r.a)(e,Q),d=Object(p.a)(t,"col"),u=[],f=[];return _.forEach((function(e){var a,t,l,r=i[e];if(delete i[e],"object"===typeof r&&null!=r){var c=r.span;a=void 0===c||c,t=r.offset,l=r.order}else a=r;var s="xs"!==e?"-"+e:"";a&&u.push(!0===a?""+d+s:""+d+s+"-"+a),null!=l&&f.push("order"+s+"-"+l),null!=t&&f.push("offset"+s+"-"+t)})),u.length||u.push(d),n.a.createElement(m,Object(l.a)({},i,{ref:a,className:s.a.apply(void 0,[c].concat(u,f))}))}));z.displayName="Col";var K=z,U=["as","bsPrefix","column","srOnly","className","htmlFor"],J=n.a.forwardRef((function(e,a){var t=e.as,c=void 0===t?"label":t,m=e.bsPrefix,i=e.column,d=e.srOnly,u=e.className,f=e.htmlFor,b=Object(r.a)(e,U),N=Object(o.useContext)(v).controlId;m=Object(p.a)(m,"form-label");var h="col-form-label";"string"===typeof i&&(h=h+" "+h+"-"+i);var E=s()(u,m,d&&"sr-only",i&&h);return f=f||N,i?n.a.createElement(K,Object(l.a)({ref:a,as:"label",className:E,htmlFor:f},b)):n.a.createElement(c,Object(l.a)({ref:a,className:E,htmlFor:f},b))}));J.displayName="FormLabel",J.defaultProps={column:!1,srOnly:!1};var B=J,H=["bsPrefix","className","as","muted"],W=n.a.forwardRef((function(e,a){var t=e.bsPrefix,c=e.className,o=e.as,m=void 0===o?"small":o,i=e.muted,d=Object(r.a)(e,H);return t=Object(p.a)(t,"form-text"),n.a.createElement(m,Object(l.a)({},d,{ref:a,className:s()(c,t,i&&"text-muted")}))}));W.displayName="FormText";var X=W,Y=n.a.forwardRef((function(e,a){return n.a.createElement(C,Object(l.a)({},e,{ref:a,type:"switch"}))}));Y.displayName="Switch",Y.Input=C.Input,Y.Label=C.Label;var Z=Y,$=t(38),ee=["bsPrefix","inline","className","validated","as"],ae=Object($.a)("form-row"),te=n.a.forwardRef((function(e,a){var t=e.bsPrefix,c=e.inline,o=e.className,m=e.validated,i=e.as,d=void 0===i?"form":i,u=Object(r.a)(e,ee);return t=Object(p.a)(t,"form"),n.a.createElement(d,Object(l.a)({},u,{ref:a,className:s()(o,m&&"was-validated",c&&t+"-inline")}))}));te.displayName="Form",te.defaultProps={inline:!1},te.Row=ae,te.Group=D,te.Control=V,te.Check=C,te.File=M,te.Switch=Z,te.Label=B,te.Text=X;a.a=te},297:function(e,a,t){"use strict";t.r(a),t.d(a,"default",(function(){return i}));var l=t(52),r=t(0),c=t.n(r),s=t(39),o=t(138),n=t(127),m=t.n(n);t(121),t(124),Object(s.a)();function i(){var e=Object(r.useState)("/dev/ttyUSB0"),a=Object(l.a)(e,2),t=a[0],s=a[1],n=Object(r.useState)(!0),i=Object(l.a)(n,2),d=i[0],u=i[1],f=Object(r.useState)(!1),b=Object(l.a)(f,2),v=b[0],p=b[1],N=Object(r.useState)(500),h=Object(l.a)(N,2),E=h[0],y=h[1],O=Object(r.useState)(10),j=Object(l.a)(O,2),g=j[0],x=j[1],C=Object(r.useState)(10),w=Object(l.a)(C,2),P=w[0],k=w[1],F=Object(r.useState)(7),I=Object(l.a)(F,2),S=I[0],T=I[1],R=Object(r.useState)(!0),M=Object(l.a)(R,2),G=M[0],L=M[1],V=Object(r.useState)("www.lengshuotech.com"),q=Object(l.a)(V,2),A=q[0],D=q[1],Q=Object(r.useState)(6200),_=Object(l.a)(Q,2),z=_[0],K=_[1],U=Object(r.useState)("www.lengshuotech.com"),J=Object(l.a)(U,2),B=J[0],H=J[1],W=Object(r.useState)(1883),X=Object(l.a)(W,2),Y=X[0],Z=X[1],$=Object(r.useState)("device/report/notify"),ee=Object(l.a)($,2),ae=ee[0],te=ee[1],le=Object(r.useState)("/host/cmd"),re=Object(l.a)(le,2),ce=re[0],se=re[1];return Object(r.useEffect)((function(){m.a.init(),setTimeout((function(){}),500)})),c.a.createElement("div",null,c.a.createElement("div",{className:"page-header"},c.a.createElement("h3",{className:"page-title"},"\u57fa\u672c\u914d\u7f6e")),c.a.createElement("div",{className:"row"},c.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},c.a.createElement("div",{className:"card"},c.a.createElement("div",{className:"card-body"},c.a.createElement("h4",{className:"card-title"},c.a.createElement("i",{className:"mdi mdi-bluetooth-settings"}),"\u7f51\u5173"),c.a.createElement("form",{className:"forms-sample"},c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"gatewayTtyName",className:"col-sm-3 col-form-label"},"\u7f51\u5173\u4e32\u53e3"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"gatewayTtyName",placeholder:"250",value:t,onChange:function(e){s(e.target.value)}}))),c.a.createElement("div",{className:"form-check"},c.a.createElement("label",{className:"form-check-label"},c.a.createElement("input",{type:"checkbox",className:"form-check-input",checked:d,onChange:function(){u(!d)},disabled:!0}),c.a.createElement("i",{className:"input-helper"}),"\u4e32\u53e3\u72b6\u6001")),c.a.createElement("div",{className:"form-check"},c.a.createElement("label",{className:"form-check-label"},c.a.createElement("input",{type:"checkbox",className:"form-check-input",checked:v,onChange:function(){p(!v)}}),c.a.createElement("i",{className:"input-helper"}),"\u81ea\u52a8\u8c03\u5ea6\u72b6\u6001")),c.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){}},"\u786e\u5b9a"))))),c.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},c.a.createElement("div",{className:"card"},c.a.createElement("div",{className:"card-body"},c.a.createElement("h4",{className:"card-title"},c.a.createElement("i",{className:"mdi mdi-bluetooth-settings"}),"\u6570\u636e\u4e0e\u65e5\u5fd7"),c.a.createElement("form",{className:"forms-sample"},c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"timeShieldCmdMS",className:"col-sm-3 col-form-label"},"\u547d\u4ee4\u63a5\u6536\u95f4\u9694(\u6beb\u79d2)"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"number",className:"form-control",id:"timeShieldCmdMS",placeholder:"250",value:E,onChange:function(e){y(parseInt(e.target.value))}}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"timeIntervalDataReportS",className:"col-sm-3 col-form-label"},"\u6570\u636e\u4e0a\u62a5\u95f4\u9694(\u79d2)"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"number",className:"form-control",id:"timeIntervalDataReportS",value:g,onChange:function(e){x(parseInt(e.target.value))},placeholder:"10"}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"dataLogKeepDays",className:"col-sm-3 col-form-label"},"\u6570\u636e\u65e5\u5fd7\u7f13\u5b58\u65f6\u95f4(\u5929)"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"number",className:"form-control",id:"dataLogKeepDays",value:P,onChange:function(e){k(parseInt(e.target.value))},placeholder:"10"}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"mqttLogKeepDays",className:"col-sm-3 col-form-label"},"MQTT\u65e5\u5fd7\u7f13\u5b58\u65f6\u95f4(\u5929)"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"number",className:"form-control",id:"mqttLogKeepDays",value:S,onChange:function(e){T(parseInt(e.target.value))},placeholder:"7"}))),c.a.createElement("div",{className:"form-check"},c.a.createElement("label",{className:"form-check-label"},c.a.createElement("input",{type:"checkbox",className:"form-check-input",checked:G,onChange:function(e){L(e.target.checked)}}),c.a.createElement("i",{className:"input-helper"}),"\u7f51\u5173\u65ad\u7ebf\u65f6\u81ea\u52a8\u91cd\u542f\u5de5\u63a7\u673a")),c.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){}},"\u786e\u5b9a"))))),c.a.createElement("div",{className:"col-md-6 grid-margin stretch-card"},c.a.createElement("div",{className:"card"},c.a.createElement("div",{className:"card-body"},c.a.createElement("h4",{className:"card-title"},c.a.createElement("i",{className:"mdi mdi-bluetooth-settings"}),"\u4e91\u670d\u52a1"),c.a.createElement("form",{className:"forms-sample"},c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"cloudServerAddress",className:"col-sm-3 col-form-label"},"\u4e91\u670d\u52a1\u5668\u5730\u5740"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"cloudServerAddress",placeholder:"\u4e91\u670d\u52a1\u5668\u5730\u5740",value:A,onChange:function(e){D(e.target.value)}}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"cloudServerPort",className:"col-sm-3 col-form-label"},"\u4e91\u670d\u52a1\u7aef\u53e3"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"number",className:"form-control",id:"cloudServerPort",value:z,onChange:function(e){K(parseInt(e.target.value))},placeholder:"10"}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"mqttServerAddress",className:"col-sm-3 col-form-label"},"MQTT\u670d\u52a1\u5668\u5730\u5740"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"mqttServerAddress",value:B,onChange:function(e){H(e.target.value)},placeholder:"MQTT\u670d\u52a1\u5668\u5730\u5740"}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"mqttServerPort",className:"col-sm-3 col-form-label"},"MQTT\u670d\u52a1\u7aef\u53e3"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"number",className:"form-control",id:"mqttServerPort",value:Y,onChange:function(e){Z(parseInt(e.target.value))},placeholder:"MQTT\u670d\u52a1\u5668\u7aef\u53e3"}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"mqttDataReportTopic",className:"col-sm-3 col-form-label"},"MQTT\u6570\u636e\u4e0a\u62a5\u4e3b\u9898"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"mqttDataReportTopic",value:ae,onChange:function(e){te(e.target.value)},placeholder:"MQTT\u6570\u636e\u4e0a\u62a5\u4e3b\u9898"}))),c.a.createElement(o.a.Group,{className:"row"},c.a.createElement("label",{htmlFor:"mqttCmdDownTopic",className:"col-sm-3 col-form-label"},"MQTT\u547d\u4ee4\u4e0b\u53d1\u4e3b\u9898"),c.a.createElement("div",{className:"col-sm-9"},c.a.createElement(o.a.Control,{type:"text",className:"form-control",id:"mqttCmdDownTopic",value:ce,onChange:function(e){se(e.target.value)},placeholder:"MQTT\u547d\u4ee4\u4e0b\u53d1\u4e3b\u9898"}))),c.a.createElement("button",{type:"button",className:"btn btn-gradient-primary mr-2",onClick:function(){}},"\u786e\u5b9a")))))))}}}]);
//# sourceMappingURL=7.5e2de09c.chunk.js.map