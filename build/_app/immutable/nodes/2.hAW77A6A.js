import{H as i}from"../chunks/control.CYgJF_JY.js";import{g as a}from"../chunks/kiseki-books-full.CHgVINyB.js";import{s as l,d as f,u,g as c,e as _}from"../chunks/scheduler.C7eb8iQI.js";import{S as p,i as m,n as d,o as g}from"../chunks/index.BLCotMXT.js";function $(s,o){throw new i(s,o)}new TextEncoder;function b({params:s}){for(const o of a){const r=o.series.find(t=>t.slug===s.series);if(r)return s.part>r.books.length&&(s.part=1),{series:r,part:s.part}}throw $(404)}const E=Object.freeze(Object.defineProperty({__proto__:null,load:b},Symbol.toStringTag,{value:"Module"}));function h(s){let o;const r=s[1].default,t=f(r,s,s[0],null);return{c(){t&&t.c()},l(e){t&&t.l(e)},m(e,n){t&&t.m(e,n),o=!0},p(e,[n]){t&&t.p&&(!o||n&1)&&u(t,r,e,e[0],o?_(r,e[0],n,null):c(e[0]),null)},i(e){o||(d(t,e),o=!0)},o(e){g(t,e),o=!1},d(e){t&&t.d(e)}}}function w(s,o,r){let{$$slots:t={},$$scope:e}=o;return s.$$set=n=>{"$$scope"in n&&r(0,e=n.$$scope)},[e,t]}class H extends p{constructor(o){super(),m(this,o,w,h,l,{})}}export{H as component,E as universal};
