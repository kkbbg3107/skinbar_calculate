import type { EmployeeWithRole, TraineeResult } from '../../types';

const FIXED_SALARY = 32042;

function calcPersonCountBonus(count: number): number {
  if (count < 110) return 0;
  let bonus = 0;
  const tier1End = Math.min(count, 132);
  if (tier1End >= 111) bonus += (tier1End - 111 + 1) * 100;
  if (count > 132) bonus += (count - 132) * 200;
  return bonus;
}

export function calcTraineeSalary(emp: EmployeeWithRole): TraineeResult {
  // 消耗×銷售獎金：業績15萬 + 消耗12萬 → 3000
  const consumptionSalesBonus =
    emp.personalPerformance >= 150000 && emp.personalConsumption >= 120000 ? 3000 : 0;

  const personCountBonus = calcPersonCountBonus(emp.personCount);
  const advancedCourseBonus = Math.round(emp.advancedCourseBonus);
  const productSalesBonus = Math.round(emp.productSalesBonus);

  const monthlyTotal = FIXED_SALARY;
  const quarterlyTotal = consumptionSalesBonus + personCountBonus + advancedCourseBonus + productSalesBonus;
  const grandTotal = monthlyTotal + quarterlyTotal;

  return {
    name: emp.name,
    role: '實習淨膚師',
    fixedSalary: FIXED_SALARY,
    consumptionSalesBonus,
    personCountBonus,
    advancedCourseBonus,
    productSalesBonus,
    monthlyTotal,
    quarterlyTotal,
    grandTotal,
  };
}
