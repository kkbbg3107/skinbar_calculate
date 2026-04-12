/** 團獎規則（正式淨膚師人數 → 業績門檻、消耗比例、每人獎金） */
export const TEAM_BONUS_RULES: Record<number, { minPerf: number; consumptionRate: number; bonus: number }> = {
  2: { minPerf: 500000,  consumptionRate: 0.75, bonus: 5000 },
  3: { minPerf: 750000,  consumptionRate: 0.75, bonus: 5600 },
  4: { minPerf: 1000000, consumptionRate: 0.75, bonus: 6000 },
  5: { minPerf: 1250000, consumptionRate: 0.75, bonus: 6250 },
  6: { minPerf: 1500000, consumptionRate: 0.75, bonus: 6500 },
};

export interface TeamBonusResult {
  qualified: boolean;
  bonusPerPerson: number;
  reason: string;
}

/**
 * Calculate team bonus.
 * numFormal: number of formal aestheticians (2-6)
 * totalPerf: total performance (formal staff only, excluding those with >12 days off)
 * totalConsumption: total consumption
 */
export function calcTeamBonus(
  numFormal: number,
  totalPerf: number,
  totalConsumption: number
): TeamBonusResult {
  const rule = TEAM_BONUS_RULES[numFormal];
  if (!rule) {
    return { qualified: false, bonusPerPerson: 0, reason: `沒有 ${numFormal} 位正式淨膚師的團獎規則` };
  }

  if (totalPerf < rule.minPerf) {
    return {
      qualified: false,
      bonusPerPerson: 0,
      reason: `業績未達標 (${totalPerf.toLocaleString()} / ${rule.minPerf.toLocaleString()})`,
    };
  }

  const consumptionRate = totalPerf > 0 ? totalConsumption / totalPerf : 0;
  if (consumptionRate < rule.consumptionRate) {
    return {
      qualified: false,
      bonusPerPerson: 0,
      reason: `消耗比例未達標 (${(consumptionRate * 100).toFixed(1)}% / ${rule.consumptionRate * 100}%)`,
    };
  }

  return {
    qualified: true,
    bonusPerPerson: rule.bonus,
    reason: `達標！每人獎金 ${rule.bonus.toLocaleString()} 元`,
  };
}
