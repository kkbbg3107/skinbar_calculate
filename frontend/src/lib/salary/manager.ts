import type { EmployeeWithRole, ManagerResult } from '../../types';

const FIXED_SALARY = 32042;
const MESSAGE_BONUS = 1500;
const MANAGEMENT_ALLOWANCE = 6000;

export function calcManagerSalary(
  emp: EmployeeWithRole,
  teamBonusPerPerson: number,
  teamQualified: boolean,
  totalPerformance: number,
  monthlyTarget: number
): ManagerResult {
  const teamBonus = teamQualified ? teamBonusPerPerson : 0;
  const targetReached = monthlyTarget > 0 && totalPerformance >= monthlyTarget;
  const achievementBonus = targetReached ? Math.round(totalPerformance * 0.0125) : 0; // 1.25%

  // 季
  const conversionRateBonus = Math.round(totalPerformance * 0.0042);     // 0.42%
  const serviceConsumptionBonus = Math.round(totalPerformance * 0.0042); // 0.42%
  const storeManagementBonus = Math.round(totalPerformance * 0.0041);    // 0.41%

  const monthlyTotal = FIXED_SALARY + teamBonus + achievementBonus + MESSAGE_BONUS + MANAGEMENT_ALLOWANCE;
  const quarterlyTotal = conversionRateBonus + serviceConsumptionBonus + storeManagementBonus;
  const grandTotal = monthlyTotal + quarterlyTotal;

  return {
    name: emp.name,
    role: '正式店長',
    fixedSalary: FIXED_SALARY,
    teamBonus,
    achievementBonus,
    messageBonus: MESSAGE_BONUS,
    managementAllowance: MANAGEMENT_ALLOWANCE,
    conversionRateBonus,
    serviceConsumptionBonus,
    storeManagementBonus,
    monthlyTotal,
    quarterlyTotal,
    grandTotal,
  };
}
