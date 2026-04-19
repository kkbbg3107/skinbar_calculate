import type { EmployeeWithRole, ExcelData, CalculationResults } from '../../types';
import { calcTeamBonus } from './teamBonus';
import { calcFormalSalary } from './formal';
import { calcTraineeSalary } from './trainee';
import { calcReserveSalary } from './reserve';
import { calcManagerSalary } from './manager';

export function calculateAll(
  employees: EmployeeWithRole[],
  excelData: ExcelData
): CalculationResults {
  const formal = employees.filter((e) => e.role === '正式淨膚師');
  const trainee = employees.filter((e) => e.role === '實習淨膚師');
  const reserve = employees.filter((e) => e.role === '儲備店長');
  const manager = employees.filter((e) => e.role === '正式店長');

  const numFormal = formal.length;
  const { qualified, bonusPerPerson } = calcTeamBonus(
    numFormal,
    excelData.totalPerformance,
    excelData.totalConsumption
  );

  return {
    formal: formal.map((emp) =>
      calcFormalSalary(emp, bonusPerPerson, qualified)
    ),
    trainee: trainee.map((emp) => calcTraineeSalary(emp)),
    reserve: reserve.map((emp) =>
      calcReserveSalary(emp, bonusPerPerson, qualified, excelData.totalPerformance, excelData.monthlyTarget, formal)
    ),
    manager: manager.map((emp) =>
      calcManagerSalary(emp, bonusPerPerson, qualified, excelData.totalPerformance, excelData.monthlyTarget)
    ),
    totalPerformance: excelData.totalPerformance,
    totalConsumption: excelData.totalConsumption,
    teamBonusPerPerson: bonusPerPerson,
    teamBonusQualified: qualified,
  };
}
