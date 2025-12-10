/**
 * Типы базовых сущностей игры "Крестики-нолики"
 */

export type CellValue = "X" | "O" | null;
export type Board = CellValue[];
export type Winner = "X" | "O" | "draw" | null;
export type PlayerSymbol = "X" | "O";
export type GameOutcome = "win" | "lose";
export interface PromoResponse {
  status: string;
  promoCode?: string;
}
