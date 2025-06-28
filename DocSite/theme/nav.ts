const nav = [
  {
    text: "主页",
    link: "/",
    activeMatch: "/index",
  },
  {
    text: "指南",
    link: "/guide/users/start",
    activeMatch: "^/guide/",
    items: [
      {
        text: "用户手册",
        link: "/guide/users/start",
        activeMatch: "^/guide/users/",
      },
      {
        text: "开发者文档",
        link: "/guide/developers/agreement",
        activeMatch: "^/guide/developers/",
      },
    ],
  },
  {
    text: "友情链接",
    items: [
      {
        text: "MaaFramework",
        link: "https://github.com/MaaXYZ/MaaFramework",
      },
      {
        text: "MFAAvalonia",
        link: "https://github.com/SweetSmellFox/MFAAvalonia",
      },
      {
        text: "YAMaaPE",
        link: "https://github.com/kqcoxn/YAMaaPE",
      },
    ],
  },
];

export default nav;
