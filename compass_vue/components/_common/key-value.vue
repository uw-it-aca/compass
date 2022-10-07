<template>
   <div :class="[mq.lgMinus ? 'justify-content-between' : '']" class="d-flex">
     <div v-if="$slots['key']" :class="[variant == 'address' ? 'text-danger' : '']" class="fw-bold text-nowrap me-2">
       <slot name="key"></slot>
     </div>
     <div v-if="$slots['value']" class="text-nowrap">
       <slot name="value"></slot>
     </div>
   </div>
 </template>

 <script>
 export default {
   inject: ["mq"],
   props: {
     variant: {
       type: String,
       default: "standard",
     },
   },
   data() {
     return {};
   },
