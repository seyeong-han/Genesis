import { createI18n } from 'vue-i18n'
import languages from '../../../locales/languages.json'

const localeFiles = import.meta.glob('../../../locales/!(languages).json', { eager: true })

const messages = {}
const availableLocales = []

for (const path in localeFiles) {
  const key = path.match(/\/([^/]+)\.json$/)[1]
  if (languages[key]) {
    messages[key] = localeFiles[path].default
    availableLocales.push({ key, label: languages[key].label })
  }
}

// Genesis is English-only. Force English regardless of any persisted locale.
const FORCED_LOCALE = 'en'
try { localStorage.setItem('locale', FORCED_LOCALE) } catch (e) { /* noop */ }

const i18n = createI18n({
  legacy: false,
  locale: FORCED_LOCALE,
  fallbackLocale: 'en',
  messages
})

export { availableLocales }
export default i18n
