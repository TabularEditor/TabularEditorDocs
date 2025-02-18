/**
 * This method will be called at the start of exports.transform in ManagedReference.html.primary.js
 */
exports.preTransform = function (model) {
  model.__header = {
    mainMenu: [
      {
        text: "Pricing",
        url: "https://tabulareditor.com/pricing"
      },
      {
        text: "Download",
        url: "https://tabulareditor.com/downloads"
      },
      {
        text: "Learn",
        url: "https://tabulareditor.com/learn"
      },
      {
        text: "Support" ,
        url: "/",
        subMenu: {
          items: [
            {
              text: "Contact",
              url: "https://tabulareditor.com/contact"
            },
            {
              text: "Newsletter",
              url: "https://tabulareditor.com/newsletter"
            },
            {
              text: "Documentation",
              url: "https://docs.tabulareditor.com/?tabs=TE3"
            }
          ]
        }
      }
    ],
    button1: {
      text: "Start free trial",
      url: "https://www.tabulareditor.com/downloads"
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
        url: "https://www.tabulareditor.com/downloads"
      },
      {
        text: "Buy Tabular Editor 3",
        url: "https://www.tabulareditor.com/pricing"
      }
    ],
    leftLinks: [
      {
        text: "About us",
        url: "https://tabulareditor.com/about-us"
      },
      {
        text: "Contact us",
        url: "https://tabulareditor.com/contact"
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
        url: "https://www.linkedin.com/company/tabular-editor/"
      },
      {
        text: "Twitter",
        url: "https://twitter.com/TabularEditor3"
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
        url: "https://tabulareditor.com/license-terms"
      }
    ]
  }
  return model;
}