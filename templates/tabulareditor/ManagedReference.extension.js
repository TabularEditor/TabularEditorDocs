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
        text: "Resources" ,
        url: "/",
        subMenu: {
          items: [
            {
              text: "Blog",
              url: "https://tabulareditor.com/blog"
            },
            {
              text: "Newsletter",
              url: "https://tabulareditor.com/newsletter"
            },
            {
              text: "Publications",
              url: "https://tabulareditor.com/publications"
            },
            {
              text: "Documentation",
              url: "https://docs.tabulareditor.com/?tabs=TE3"
            },
            {
              text: "Support community",
              url: "https://github.com/TabularEditor/TabularEditor3"
            }
          ]
        }
      },
      {
        text: "Contact Us",
        url: "https://tabulareditor.com/contact"
      }
    ],
    button1: {
      text: "Free trial",
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
        url: "https://www.linkedin.com/company/tabular-editor/",
        svg: '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" fill="none">  <path d="M24.9227 18.6686C25.1868 18.6657 25.4501 18.6989 25.7052 18.7672C25.9159 18.825 26.1154 18.9178 26.2952 19.0418C26.6233 19.2794 26.8719 19.6105 27.0085 19.9918C27.1586 20.4011 27.2493 20.8297 27.2779 21.2647C27.3166 21.7006 27.3197 22.1479 27.3197 22.6062V29.8252H31.9297L31.9317 21.6814C31.9317 19.3127 31.6187 17.7599 30.9169 16.6466C30.0531 15.2766 28.575 14.6103 26.3981 14.6103C26.3382 14.608 26.2769 14.6069 26.2175 14.6069C25.3713 14.6087 24.5402 14.8311 23.8062 15.2522C23.0722 15.6734 22.4607 16.2786 22.0321 17.0083H21.9701V14.9794H17.5449V29.8245H22.1549V22.4807C22.1492 22.0081 22.181 21.5357 22.2498 21.0681C22.3079 20.642 22.4395 20.2292 22.6387 19.8481C22.7347 19.6718 22.8536 19.509 22.9922 19.3638C23.1346 19.2162 23.2982 19.0908 23.4778 18.9916C23.6779 18.8826 23.8924 18.8022 24.1149 18.7527C24.3801 18.6945 24.6511 18.6663 24.9227 18.6686ZM10.0339 14.9794V29.825H14.6484V14.9794H10.0339ZM12.3431 7.60001C11.814 7.60001 11.2968 7.7569 10.8569 8.05084C10.4169 8.34478 10.0741 8.76258 9.8716 9.25139C9.66913 9.7402 9.61615 10.2781 9.71937 10.797C9.82259 11.3159 10.0774 11.7926 10.4515 12.1667C10.8256 12.5408 11.3023 12.7956 11.8212 12.8988C12.3401 13.002 12.878 12.949 13.3668 12.7466C13.8556 12.5441 14.2734 12.2012 14.5673 11.7613C14.8613 11.3214 15.0182 10.8042 15.0182 10.2751C15.0174 9.56587 14.7353 8.88591 14.2338 8.3844C13.7323 7.88289 13.0523 7.6008 12.3431 7.60001Z" fill="white"></path></svg>'
      },
      {
        text: "Twitter",
        url: "https://twitter.com/TabularEditor3",
        svg: '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">  <path d="M17.0336 20.6249L21.7372 26.775H27.7447L20.0724 16.633L26.5934 9.18002H23.6094L18.6909 14.8032L14.4375 9.18002H8.2793L15.6385 18.8031L8.66369 26.775H11.6503L17.0336 20.6249ZM24.2151 24.9886H22.5623L11.7648 10.8736H13.5397L24.2151 24.9886Z" fill="white"></path></svg>'
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
