import * as path from "node:path";
import { defineConfig } from "rspress/config";

import nav from "./theme/nav";
import sidebar from "./theme/sidebar";

export default defineConfig({
  root: path.join(__dirname, "docs"),
  base: "/mnma/",
  title: "MNMA文档站",
  logoText: "MNMA文档站",
  icon: "/logo.ico",
  logo: "/logo.png",
  lang: "zh-CN",
  themeConfig: {
    nav,
    sidebar,
    enableScrollToTop: true,
    socialLinks: [
      {
        icon: "github",
        mode: "link",
        content: "https://github.com/kqcoxn/MaaNewMoonAccompanying",
      },
    ],
  },
});
