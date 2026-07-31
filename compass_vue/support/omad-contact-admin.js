// Copyright 2026 UW-IT, University of Washington
// SPDX-License-Identifier: Apache-2.0

import { createApp } from "vue";

if (typeof window.supporttoolsRegisterSpaTool !== "function") {
  window.supporttoolsRegisterSpaTool = function (componentKey, importFn) {
    window.supporttoolsSpaComponents = window.supporttoolsSpaComponents || {};
    window.supporttoolsSpaComponents[componentKey] = importFn;

    const target = document.getElementById("spa-tool-app");
    if (!target) {
      return;
    }

    importFn().then(function (mod) {
      const component = mod && (mod.default || mod);
      if (component) {
        createApp(component).mount(target);
      }
    });
  };
}

window.supporttoolsRegisterSpaTool("omad_contact_admin", () =>
  import("./OMADContactAdmin.vue")
);
