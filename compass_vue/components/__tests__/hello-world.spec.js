import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import HelloWorld from "../hello-world.vue";

describe("Hello World", () => {
  it("displays hello world", () => {
    const wrapper = mount(HelloWorld);
    // Assert the rendered text of the component
    expect(wrapper.text()).toContain("Hello world");
  });
});
