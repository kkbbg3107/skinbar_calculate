import type { EmployeeWithRole, FormalResult } from '../../types';

const FIXED_SALARY = 32042;

/** 人次激勵獎金 */
function calcPersonCountBonus(count: number): number {
  if (count < 110) return 0;
  let bonus = 0;
  const tier1End = Math.min(count, 132);
  if (tier1End >= 111) bonus += (tier1End - 111 + 1) * 100;
  if (count > 132) bonus += (count - 132) * 200;
  return bonus;
}

/** 充值目標達成獎 (需面膜7組) */
function calcChargeTargetBonus(performance: number, maskCount: number): { bonus: number; reason: string } {
  if (maskCount < 7) return { bonus: 0, reason: `面膜未達責任額 ${maskCount}/7 組` };
  if (performance >= 300000) return { bonus: 7000, reason: `業績30萬+面膜${maskCount}組達標` };
  if (performance >= 250000) return { bonus: 2000, reason: `業績25萬+面膜${maskCount}組達標` };
  return { bonus: 0, reason: `業績未達25萬 (${performance.toLocaleString()})` };
}

/** 個人消耗獎勵 */
function calcConsumptionBonus(consumption: number): { bonus: number; reason: string } {
  if (consumption >= 200000) {
    return { bonus: Math.floor(consumption * 0.025), reason: `消耗20萬達標，2.5%` };
  }
  if (consumption >= 180000) {
    return { bonus: Math.floor(consumption * 0.015), reason: `消耗18萬達標，1.5%` };
  }
  return { bonus: 0, reason: `消耗未達18萬 (${consumption.toLocaleString()})` };
}

/** 消耗充值雙達標獎 */
function calcDualTargetBonus(
  consumption: number,
  performance: number,
  maskCount: number
): { bonus: number; reason: string } {
  const { bonus: chargeB } = calcChargeTargetBonus(performance, maskCount);
  const { bonus: consumptionB } = calcConsumptionBonus(consumption);
  if (chargeB > 0 && consumptionB > 0) {
    return { bonus: 2000, reason: '充值+消耗雙達標' };
  }
  return { bonus: 0, reason: '未同時達標' };
}

/** 新客成交率70%獎金 */
function calcNewCustomerRateBonus(
  personCount: number,
  newCustomerRate: number
): { bonus: number; reason: string } {
  const rate = newCustomerRate > 1 ? newCustomerRate / 100 : newCustomerRate;
  if (personCount < 132) return { bonus: 0, reason: `人次未達132 (${personCount.toFixed(0)})` };
  if (rate < 0.7) return { bonus: 0, reason: `成交率未達70% (${(rate * 100).toFixed(1)}%)` };
  return { bonus: 4000, reason: `人次+成交率達標` };
}

/** 檢查3項指標是否未達2項（未達2項 = 失去團獎資格）*/
function checkMetricsDisqualification(emp: EmployeeWithRole): { disqualified: boolean; failedMetrics: string[] } {
  const toRate = (v: number) => v > 1 ? v / 100 : v;

  const failed: string[] = [];
  if (toRate(emp.newCustomerRate) < 0.70) failed.push(`新客成交率 ${(toRate(emp.newCustomerRate) * 100).toFixed(1)}% < 70%`);
  if (toRate(emp.vipUpgradeRate) < 0.65)  failed.push(`VIP升單率 ${(toRate(emp.vipUpgradeRate) * 100).toFixed(1)}% < 65%`);
  if (toRate(emp.appointmentRate) < 0.70) failed.push(`預約率 ${(toRate(emp.appointmentRate) * 100).toFixed(1)}% < 70%`);

  return { disqualified: failed.length >= 2, failedMetrics: failed };
}

export function calcFormalSalary(
  emp: EmployeeWithRole,
  maskSales: Record<string, number>,
  teamBonusPerPerson: number,
  teamQualified: boolean
): FormalResult {
  const maskCount = maskSales[String(emp.therapistId)] ?? 0;

  // 3項指標個人資格檢查
  const { disqualified, failedMetrics } = checkMetricsDisqualification(emp);

  // 團獎
  let teamBonus = (teamQualified && !disqualified) ? teamBonusPerPerson : 0;
  let teamBonusDeduction = 0;
  if (teamQualified && !disqualified && emp.personalPerformance < 180000) {
    teamBonusDeduction = 2000;
    teamBonus = Math.max(0, teamBonus - 2000);
  }

  // 季獎金
  const personCountBonus = calcPersonCountBonus(emp.personCount);
  const { bonus: chargeTargetBonus } = calcChargeTargetBonus(emp.personalPerformance, maskCount);
  const { bonus: consumptionBonus } = calcConsumptionBonus(emp.personalConsumption);
  const { bonus: dualTargetBonus } = calcDualTargetBonus(
    emp.personalConsumption, emp.personalPerformance, maskCount
  );
  const advancedCourseBonus = Math.round(emp.advancedCourseBonus);
  const productSalesBonus = Math.round(emp.productSalesBonus);
  const { bonus: newCustomerRateBonus } = calcNewCustomerRateBonus(
    emp.personCount, emp.newCustomerRate
  );

  const monthlyTotal = FIXED_SALARY + emp.skillBonusTotal + teamBonus;
  const quarterlyTotal =
    personCountBonus + chargeTargetBonus + consumptionBonus + dualTargetBonus +
    advancedCourseBonus + productSalesBonus + newCustomerRateBonus;
  const grandTotal = monthlyTotal + quarterlyTotal;

  return {
    name: emp.name,
    role: '正式淨膚師',
    fixedSalary: FIXED_SALARY,
    skillBonus: Math.round(emp.skillBonusTotal),
    teamBonus,
    teamBonusDeduction,
    teamBonusDisqualified: disqualified,
    failedMetrics,
    personCountBonus,
    chargeTargetBonus,
    consumptionBonus,
    dualTargetBonus,
    advancedCourseBonus,
    productSalesBonus,
    newCustomerRateBonus,
    monthlyTotal,
    quarterlyTotal,
    grandTotal,
  };
}
