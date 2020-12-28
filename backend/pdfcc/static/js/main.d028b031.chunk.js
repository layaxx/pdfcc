(this["webpackJsonpreact-typescript"]=this["webpackJsonpreact-typescript"]||[]).push([[0],{30:function(e,t,r){},31:function(e,t,r){},34:function(e,t,r){},35:function(e,t,r){},36:function(e,t,r){},40:function(e,t,r){},43:function(e,t,r){"use strict";r.r(t);var o=r(1),n=r(0),s=r.n(n),a=r(10),i=r.n(a),l=(r(30),r(11)),c=r(20),u=r(21),d=r(24),p=r(22),f=r(7),m=(r(12),r(14)),b=r(15),j=r(13);r(31);var h=function(e){var t=Object(n.useState)(!1),r=Object(f.a)(t,2),s=r[0],a=r[1],i=Object(n.useState)({}),l=Object(f.a)(i,2),c=l[0],u=l[1],d=Object(n.useState)({message:"",type:""}),p=Object(f.a)(d,2),h=p[0],g=p[1];return Object(o.jsxs)("div",{children:[Object(o.jsx)("h4",{className:"mb-3",children:"PDF Document"}),Object(o.jsxs)("form",{encType:"multipart/form-data",id:"id_ajax_upload_form",method:"POST",noValidate:!0,children:[Object(o.jsx)("label",{htmlFor:"input_pdf",children:"Choose a PDF Document: "}),Object(o.jsx)("br",{}),Object(o.jsx)("input",{id:"input_pdf",type:"file",accept:"application/pdf",onChange:function(e){var t;(function(e){var t,r,o,n=null===e||void 0===e||null===(t=e.target)||void 0===t||null===(r=t.files)||void 0===r||null===(o=r.item(0))||void 0===o?void 0:o.size;return"undefined"!==typeof n&&"number"===typeof n&&(!(n>15728640)||(g({message:"The size of the PDF must be 15 MB or less",type:"warning"}),!1))})(e)&&null!=e.target.files?(u(e.target.files[0]),a(!0),g({message:"",type:""})):(a(!1),null===(t=document.getElementById("id_ajax_upload_form"))||void 0===t||t.reset())},required:!0}),Object(o.jsx)("div",{className:"status-wrapper",children:Object(o.jsxs)(b.a,{variant:h.type,id:"submit-status",hidden:""===h.type,children:[Object(o.jsx)(j.a,{animation:"border",role:"status",hidden:"Waiting for Server response"!==h.message}),h.message]})}),Object(o.jsx)(m.a,{id:"submit-pdf",type:"submit",block:!0,onClick:function(t){if(t.preventDefault(),s){var r=new FormData,o=c;r.append("file",o),g({message:"Waiting for Server response",type:"info"}),fetch("/ajax/react",{method:"POST",body:r}).then((function(e){if(!e.ok)throw Error(e.statusText);return e})).then((function(e){return e.json()})).then((function(t){t.error?g({message:"Server responded with error message: "+t.message,type:"danger"}):e.showColors(t.analysis_result,c)})).catch((function(e){g({message:e,type:"danger"})}))}else g({message:"Please select a Document first",type:"warning"})},disabled:"Waiting for Server response"===h.message,children:"Waiting for Server response"!==h.message?"Submit Document":"Waiting..."})]})]})},g=(r(34),r(35),["Choose PDF","Choose Colors","Download your new PDF!"]);var v=function(e){for(var t=[],r=0;r<3;r++)t.push(Object(o.jsxs)("li",{id:"progress-"+r,className:"list-group-item flex-fill "+(r===e.progress?"list-group-item-primary":"")+(r<e.progress?"list-group-item-secondary":""),children:[" ",g[r]]},r));return Object(o.jsx)("div",{className:"progress-wrapper",children:Object(o.jsx)("ul",{className:"list-group list-group-horizontal",children:t})})},O=r(17),C=r(23);r(36);var x=function(e){var t="input-"+e.color,r="pre-"+e.color,s=Object(n.useState)(""),a=Object(f.a)(s,2),i=a[0],c=a[1],u=Object(l.a)({},"backgroundColor",e.color);return Object(o.jsxs)("div",{children:[Object(o.jsxs)("div",{className:"colorcode",style:u,children:[Object(o.jsx)("div",{id:r,className:"right-side",style:{backgroundColor:i,display:""===i?"None":"block"}}),Object(o.jsx)("p",{onClick:function(e){var t=e.target,r=document.createElement("input");r.value=null!=t.textContent?t.textContent:"",t.after(r),r.select(),document.execCommand("copy"),r.remove()},children:e.color})]}),Object(o.jsx)("p",{className:"pages",children:e.pages}),Object(o.jsxs)(O.a,{children:[Object(o.jsx)(O.a.Prepend,{children:Object(o.jsx)(O.a.Text,{id:t,children:"#"})}),Object(o.jsx)(C.a,{placeholder:"new Color","aria-placeholder":"new Color","aria-label":"new Color","aria-describedby":t,onBlur:function(t){var r,o,n=t.target.value,s=(null===(r=t.target)||void 0===r||null===(o=r.parentNode)||void 0===o?void 0:o.children[0].children[0]).style;0!==n.length&&6!==n.length&&7!==n.length&&(s.backgroundColor="#dc3545",s.color="white",e.updateColors(e.color,null),c(""))},onChange:function(t){var r,o,n=t.target.value,s=(null===(r=t.target)||void 0===r||null===(o=r.parentNode)||void 0===o?void 0:o.children[0].children[0]).style;0===n.length?""===n&&(s.backgroundColor="#e9ecef",s.color="black",e.updateColors(e.color,""),c("")):6!==n.length&&7!==n.length||(!function(e){if(6===e.length){for(var t=0;t<6;t++)if(!((o=e.charAt(t))>="a"&&o<="f"||o>="A"&&o<="F"||o>="0"&&o<="9"))return!1;return!0}if(7===e.length&&"#"===e.charAt(0)){for(var r=1;r<7;r++)if(e.charAt(r)<"a"||e.charAt(r)<"f")return!1;return!0}var o;return!1}(n)?(s.backgroundColor="#dc3545",s.color="white",e.updateColors(e.color,null),c("")):(s.backgroundColor="#28a745",s.color="white",e.updateColors(e.color,n),c("#"+n)))}})]})]})},y=(r(40),r(41),r(9)),w=r.n(y);var S=function(e){var t=e.state(),r=t.colors,s=t.file,a=Object(n.useState)({mapOldColorsToNewColors:new Map,errors:new Set,alert:{type:"danger",msg:"You submitted invalid new colors for: ",active:!1},waitingForServerResponse:!1}),i=Object(f.a)(a,2),l=i[0],c=i[1],u=[];for(var d in r)u.push(Object(o.jsx)(x,{updateColors:function(e,t){c(null===t?function(t){return w()(t,{mapOldColorsToNewColors:{$remove:[e]},errors:{$add:[e]}})}:""===t?function(t){return w()(t,{mapOldColorsToNewColors:{$remove:[e]},errors:{$remove:[e]}})}:function(r){return w()(r,{mapOldColorsToNewColors:{$add:[[e,t]]},errors:{$remove:[e]}})})},color:r[d][0],pages:r[d][1]},d));return Object(o.jsxs)("form",{id:"form-colors",autoComplete:"off",children:[Object(o.jsxs)("p",{children:[Object(o.jsx)("b",{children:"Showing Colors for: "}),s.name]}),Object(o.jsx)("div",{className:"analysis_result",children:u}),Object(o.jsx)("div",{className:"status-wrapper",children:Object(o.jsxs)(b.a,{variant:l.alert.type,id:"submit-status",hidden:0===l.errors.size&&!l.alert.active,children:[Object(o.jsx)(j.a,{animation:"border",role:"status",hidden:"Waiting for Server response..."!==l.alert.msg}),l.alert.msg+(0!==l.errors.size?Array.from(l.errors).join(", "):"")]})}),Object(o.jsx)(m.a,{type:"submit",onClick:function(t){if(t.preventDefault(),0!==l.errors.size){var r=document.querySelector("#submit-status");null===r||void 0===r||r.classList.add("animate__animated","animate__pulse"),setTimeout((function(){null===r||void 0===r||r.classList.remove("animate__pulse")}),1e3)}else if(l.mapOldColorsToNewColors.size>0){c((function(e){return w()(e,{alert:{active:{$set:!0},type:{$set:"info"},msg:{$set:"Waiting for Server response..."}}})}));var o=new FormData,n=s;o.append("file",n),l.mapOldColorsToNewColors.forEach((function(e,t){o.append(t,e)})),fetch("/ajax/process",{method:"POST",body:o}).then((function(e){if(!e.ok)throw Error(e.statusText);return e})).then((function(e){return e.json()})).then((function(t){t.error?c((function(e){return w()(e,{alert:{active:{$set:!0},type:{$set:"danger"},msg:{$set:"Request came back with the following error message: "+t.message}}})})):e.handleChange(t.b64)})).catch((function(e){c((function(t){return w()(t,{alert:{active:{$set:!0},type:{$set:"danger"},msg:{$set:"Request failed: "+e}}})}))}))}},block:!0,disabled:"Waiting for Server response..."===l.alert.msg,children:"Waiting for Server response..."!==l.alert.msg?"Submit Colors":"Waiting..."})]})};var D,N=function(e){var t=e.oldFileName(),r=(null===t||void 0===t?void 0:t.split(".pdf")[0])+"-printable";return Object(o.jsxs)("div",{children:[Object(o.jsx)("h4",{className:"mb-3",children:"PDF Document"}),Object(o.jsx)("a",{href:"data:application/pdf;base64,"+e.b64(),className:"btn btn-success btn-block",download:r,children:"Download your new PDF!"})]})};!function(e){e[e.initial=0]="initial",e[e.submittedPDF=1]="submittedPDF",e[e.submittedColors=2]="submittedColors"}(D||(D={}));var F=function(e){Object(d.a)(r,e);var t=Object(p.a)(r);function r(e){var n,s;return Object(c.a)(this,r),(s=t.call(this,e)).componentsByProgress=(n={},Object(l.a)(n,D.initial,Object(o.jsx)(h,{showColors:function(e,t){s.setState({colors:e,progress:D.submittedPDF,file:t})}})),Object(l.a)(n,D.submittedPDF,Object(o.jsx)(S,{state:function(){return s.state},handleChange:function(e){s.setState({b64:e,progress:D.submittedColors})}})),Object(l.a)(n,D.submittedColors,Object(o.jsx)(N,{b64:function(){return s.state.b64},oldFileName:function(){var e;return null===(e=s.state.file)||void 0===e?void 0:e.name}})),n),s.state={colors:null,progress:D.initial,file:null,b64:""},s}return Object(u.a)(r,[{key:"displayWarning",value:function(e){alert(e)}},{key:"render",value:function(){return Object(o.jsxs)("div",{children:[Object(o.jsx)(v,{progress_enum:D,progress:this.state.progress}),this.componentsByProgress[this.state.progress]]})}}]),r}(s.a.Component),k=function(e){e&&e instanceof Function&&r.e(3).then(r.bind(null,45)).then((function(t){var r=t.getCLS,o=t.getFID,n=t.getFCP,s=t.getLCP,a=t.getTTFB;r(e),o(e),n(e),s(e),a(e)}))};i.a.render(Object(o.jsx)(s.a.StrictMode,{children:Object(o.jsx)(F,{})}),document.getElementById("root")),k()}},[[43,1,2]]]);
//# sourceMappingURL=main.d028b031.chunk.js.map