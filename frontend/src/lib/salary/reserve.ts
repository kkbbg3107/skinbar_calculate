import type { EmployeeWithRole, ReserveResult } from '../../types';

const FIXED_SALARY = 32042;
const MESSAGE_BONUS = 1500;

/** 淨膚師目標達成獎：所有正式淨膚師都達成 消耗18萬/業績25萬/人次132 → 5,000 */
export function allFormalGoalsAchieved(
  formalEmployees: EmployeeWithRole[]
): boolean {
  return formalEmployees.every(
    (e) =>
      e.personalConsumption >= 180000 &&
      e.personalPerformance >= 250000 &&
      e.personCount >= 132
  );
}

export function calcReserveSalary(
  emp: EmployeeWithRole,
  teamBonusPerPerson: number,
  teamQualified: boolean,
  totalPerformance: number,
  monthlyTarget: number,
  formalEmployees: EmployeeWithRole[]
): ReserveResult {
  const teamBonus = teamQualified ? teamBonusPerPerson : 0;
  const targetReached = monthlyTarget > 0 && totalPerformance >= monthlyTarget;
  const achievementBonus = targetReached ? Math.round(totalPerformance * 0.01) : 0;
  const messageBonus = MESSAGE_BONUS;

  // 季
  const conversionRateBonus = Math.round(totalPerformance * 0.0034);
  const serviceConsumptionBonus = Math.round(totalPerformance * 0.0033);
  const storeManagementBonus = Math.round(totalPerformance * 0.0033);
  const therapistGoalBonus = allFormalGoalsAchieved(formalEmployees) ? 5000 : 0;

  const monthlyTotal = FIXED_SALARY + teamBonus + achievementBonus + messageBonus;
  const quarterlyTotal = conversionRateBonus + serviceConsumptionBonus + storeManagementBonus + therapistGoalBonus;
  const grandTotal = monthlyTotal + quarterlyTotal;

  return {
    name: emp.name,
    role: '儲備店長',
    fixedSalary: FIXED_SALARY,
    teamBonus,
    achievementBonus,
    messageBonus,
    conversionRateBonus,
    serviceConsumptionBonus,
    storeManagementBonus,
    therapistGoalBonus,
    monthlyTotal,
    quarterlyTotal,
    grandTotal,
  };
}
