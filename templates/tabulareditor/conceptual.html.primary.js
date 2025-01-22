exports.transform = function (model) {
  // model._appLogoPath = "images/tabular-editor-logo.svg"
  model.__header = {
    mainMenu: [
      {
        text: "Pricing",
        url: "/"
      },
      {
        text: "Download",
        url: "/download"
      },
      {
        text: "Learn",
        url: "/learn"
      },
      {
        text: "Support" ,
        url: "/support",
        subMenu: {
          items: [
            {
              text: "Contact",
              url: "/support/contact"
            },
            {
              text: "Newsletter",
              url: "/support/newsletter"
            },
            {
              text: "Documentation",
              url: "https://docs.tabulareditor.com"
            }
          ]
        }
      }
    ],
    button1: {
      text: "Start free trial",
      url: "https://www.tabulareditor.com"
    },
    button2: {
      text: "Sign in",
      url: "https://www.tabulareditor.com"
    },
  }

  model.__footer = {
    buttons: [
      {
        text: "Try Tabular Editor 3 for free",
        url: "https://www.tabulareditor.com"
      },
      {
        text: "Buy Tabular Editor 3",
        url: "https://www.tabulareditor.com"
      }
    ],
    leftLinks: [
      {
        text: "About us",
        url: "https://www.tabulareditor.com/about"
      },
      {
        text: "Contact us",
        url: "https://www.tabulareditor.com/contact"
      },
      {
        text: "Technical Support",
        url: "mailto:support@tabulareditor.com",
        rel: "noopener noreferrer",
        target: "_blank"
      }
    ],
    rightLinks: [
      {
        text: "LinkedIn",
        url: "https://www.tabulareditor.com/privacy"
      },
      {
        text: "Twitter",
        url: "https://www.tabulareditor.com/tos"
      }
    ],
    bottomLinks: [
      {
        text: "Privacy & Cookie policy",
        url: "https://tabulareditor.com/privacy-policy"
      },
      {
        text: "Terms & Conditions",
        url: "https://tabulareditor.com/terms"
      },
      {
        text: "License terms",
        url: "https://tabulareditor.com/assets/Tabular-Editor-Standard-License-Terms-version-2.0-November-2024-DutNQkZq.pdf"
      }
    ]
  }

  return model;
}
