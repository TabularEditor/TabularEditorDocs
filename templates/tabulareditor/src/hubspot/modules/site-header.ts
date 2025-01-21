// ===========================
// main header search form
// ===========================
export function headerSearch(): void {
  const headerSearch = document.getElementById('headerSearch');
  if (!headerSearch) return;

  const searchForm = headerSearch.querySelector('.header-search__form') as HTMLFormElement;
  const searchFormInput = headerSearch.querySelector('.header-search__form-input') as HTMLInputElement;
  const searchFormBtn = headerSearch.querySelector('.header-search__form-btn') as HTMLButtonElement;
  const searchResults = headerSearch.querySelector('.header-search__suggestions') as HTMLElement;

  function showSearchForm(event: Event, elem: HTMLElement, isPreventDefault: boolean): void {
    if (!elem.classList.contains('header-search--show')) {
      elem.classList.add('header-search--show');
      if (!document.body.classList.contains('open-search_wrp')) {
        document.body.classList.add('open-search_wrp');
      }
      if (searchForm.tabIndex === 0) {
        searchForm.tabIndex = -1;
      }
      if (searchFormBtn.tabIndex === -1) {
        searchFormBtn.tabIndex = 0;
      }
      if (searchFormInput.tabIndex === -1) {
        searchFormInput.tabIndex = 0;
      }
      searchFormInput.focus();
      if (isPreventDefault) {
        event.preventDefault();
      }
    }
  }

  function hideSearchForm(event: Event, elem: HTMLElement, isPreventDefault: boolean): void {
    if (elem.classList.contains('header-search--show')) {
      elem.classList.remove('header-search--show');
      if (document.body.classList.contains('open-search_wrp')) {
        document.body.classList.remove('open-search_wrp');
      }
      if (elem.classList.contains('header-search--open')) {
        elem.classList.remove('header-search--open');
        searchResults.innerHTML = '';
      }
      if (searchForm.tabIndex === -1) {
        searchForm.tabIndex = 0;
      }
      if (searchFormBtn.tabIndex === 0) {
        searchFormBtn.tabIndex = -1;
      }
      if (searchFormInput.tabIndex === 0) {
        searchFormInput.tabIndex = -1;
      }
      searchFormInput.blur();
      searchFormInput.value = '';
      if (isPreventDefault) {
        event.preventDefault();
      }
    }
  }

  function showSearchFormBySbmBtn(event: Event): void {
    if (headerSearch.classList.contains('header-search--show')) {
      hideSearchForm(event, headerSearch, true);
    } else {
      showSearchForm(event, headerSearch, true);
    }
  }
  searchFormBtn.addEventListener('click', showSearchFormBySbmBtn, { once: false, passive: false });

  function showSearchFormByFocus(event: Event): void {
    showSearchForm(event, headerSearch, false);
  }
  searchFormInput.addEventListener('focus', showSearchFormByFocus, { once: false, passive: true });

  function showSearchFormByKeyEnter(event: KeyboardEvent): void {
    if (event.code === 'Enter') {
      showSearchForm(event, headerSearch, false);
    }
  }
  searchForm.addEventListener('keyup', showSearchFormByKeyEnter, { once: false, passive: true });

  function hideSearchFormByKeyEscape(event: KeyboardEvent): void {
    if (event.code === 'Escape') {
      hideSearchForm(event, headerSearch, false);
    }
  }
  document.addEventListener('keyup', hideSearchFormByKeyEscape, { once: false, passive: true });

  function hideSearchFormByBlur(event: FocusEvent): void {
    if (event.relatedTarget && !(event.relatedTarget as HTMLElement).closest('.header-search__form_wrp')) {
      hideSearchForm(event, headerSearch, false);
    }
  }
  searchFormInput.addEventListener('blur', hideSearchFormByBlur, { once: false, passive: true });
  searchFormBtn.addEventListener('blur', hideSearchFormByBlur, { once: false, passive: true });

  function hideSearchFormByClick(event: MouseEvent): void {
    if (!event.target.closest('.header-search__form_wrp')) {
      hideSearchForm(event, headerSearch, false);
    }
  }
  document.addEventListener('click', hideSearchFormByClick, { once: false, passive: true });
}
