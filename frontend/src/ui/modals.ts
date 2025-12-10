/**
 * Управление модальными окнами (в частности, победным промо-окном)
 */

const promoModalEl = document.getElementById("promo-modal") as HTMLElement;
const promoCodeEl = document.getElementById("promo-code") as HTMLElement;
const promoPlayAgainBtn = document.getElementById(
  "promo-play-again"
) as HTMLButtonElement;

type PromoModalHandlers = {
  onPlayAgain?: () => void;
};

let handlers: PromoModalHandlers = {};

/**
 * Контроллер модалки промокода
 */
export const promoModal = {
  /**
   * Показать модальное окно с промокодом
   */
  show(code: string) {
    promoCodeEl.textContent = code;
    promoModalEl.classList.remove("promo-modal--hidden");
  },

  /**
   * Скрыть окно
   */
  hide() {
    promoModalEl.classList.add("promo-modal--hidden");
  },

  /**
   * Установить обработчики внешних событий
   */
  setHandlers(newHandlers: PromoModalHandlers) {
    handlers = newHandlers;
  },
};

/**
 * Кнопка "Play Again" внутри промо-модалки
 */
promoPlayAgainBtn.addEventListener("click", () => {
  promoModal.hide();
  handlers.onPlayAgain?.();
});
