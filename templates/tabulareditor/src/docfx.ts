// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

import 'bootstrap'
import { options } from './helper'
import { highlight } from './highlight'
import { renderMarkdown } from './markdown'
import { enableSearch } from './search'
import { renderToc } from './toc'
import { initTheme } from './theme'
import { renderBreadcrumb, renderInThisArticle, renderNavbar } from './nav'
import { headerSearch } from './hubspot/modules/site-header'
import 'bootstrap-icons/font/bootstrap-icons.scss'
import './docfx.scss'
import './local.scss'
import SimpleLightbox from "simplelightbox";
// import SimpleLightbox from 'simplelightbox/dist/simple-lightbox.esm'

declare global {
  interface Window {
    docfx: {
      ready?: boolean,
      searchReady?: boolean,
      searchResultReady?: boolean,
    }
  }
}

async function init() {
  window.docfx = window.docfx || {}

  const { start } = await options()
  start?.()

  const pdfmode = navigator.userAgent.indexOf('docfx/pdf') >= 0
  if (pdfmode) {
    await Promise.all([
      renderMarkdown(),
      highlight()
    ])
  } else {
    await Promise.all([
      initTheme(),
      enableSearch(),
      renderInThisArticle(),
      renderMarkdown(),
      renderNav(),
      highlight()
    ])
  }

  window.docfx.ready = true

  async function renderNav() {
    const [navbar, toc] = await Promise.all([renderNavbar(), renderToc()])
    renderBreadcrumb([...navbar, ...toc])
  }
  headerSearch()
  document.querySelectorAll('article a').forEach(a => {
    if (a.querySelector('img')) {
      // Add lightbox to the <a> tags that have <img> as a child
      new SimpleLightbox(a, { /* options */ })
    }
  });
}

init().catch(console.error)
