export type Role = '正式淨膚師' | '實習淨膚師' | '儲備店長' | '正式店長';

export interface RawEmployee {
  row: number;
  name: string;
  personalPerformance: number;
  personalConsumption: number;
  personCount: number;
  newCustomerRate: number;   // I欄：新客成交率
  vipUpgradeRate: number;    // R欄：VIP成交率
  appointmentRate: number;   // X欄：預約率
  advancedCourseBonus: number;
  skillBonusTotal: number;
  productSalesBonus: number;
}

export interface EmployeeWithRole extends RawEmployee {
  role: Role;
  therapistId: number; // 1-based index among formal aestheticians
}

export interface ExcelData {
  employees: RawEmployee[];
  totalPerformance: number;
  totalConsumption: number;
  monthlyTarget: number;             // E23：當月目標
  maskSales: Record<string, number>; // therapistId -> count
}

// ─── Result types ───────────────────────────────────────────────

export interface FormalResult {
  name: string;
  role: '正式淨膚師';
  fixedSalary: number;        // 32,042
  skillBonus: number;         // W 欄
  teamBonus: number;             // 團獎
  teamBonusDeduction: number;    // -2000 if perf < 180k but team qualified
  teamBonusDisqualified: boolean; // 3項指標未達2項
  failedMetrics: string[];        // 未達標的指標名稱
  // 季獎金
  personCountBonus: number;
  chargeTargetBonus: number;
  consumptionBonus: number;
  dualTargetBonus: number;
  advancedCourseBonus: number;
  productSalesBonus: number;
  newCustomerRateBonus: number;
  // totals
  monthlyTotal: number;
  quarterlyTotal: number;
  grandTotal: number;
}

export interface TraineeResult {
  name: string;
  role: '實習淨膚師';
  fixedSalary: number;
  consumptionSalesBonus: number; // 消耗×銷售獎金
  personCountBonus: number;
  advancedCourseBonus: number;
  productSalesBonus: number;
  monthlyTotal: number;
  quarterlyTotal: number;
  grandTotal: number;
}

export interface ReserveResult {
  name: string;
  role: '儲備店長';
  fixedSalary: number;
  teamBonus: number;          // 月
  achievementBonus: number;   // 達標獎金 1% (月)
  messageBonus: number;       // 訊息管理 1,500 (月)
  // 季
  conversionRateBonus: number;    // 0.34%
  serviceConsumptionBonus: number; // 0.33%
  storeManagementBonus: number;   // 0.33%
  therapistGoalBonus: number;     // 淨膚師目標達成獎 5,000
  monthlyTotal: number;
  quarterlyTotal: number;
  grandTotal: number;
}

export interface ManagerResult {
  name: string;
  role: '正式店長';
  fixedSalary: number;
  teamBonus: number;           // 月
  achievementBonus: number;    // 1.25% (月)
  messageBonus: number;        // 1,500 (月)
  managementAllowance: number; // 6,000 (月)
  // 季
  conversionRateBonus: number;    // 0.42%
  serviceConsumptionBonus: number; // 0.42%
  storeManagementBonus: number;   // 0.41%
  monthlyTotal: number;
  quarterlyTotal: number;
  grandTotal: number;
}

export type AnyResult = FormalResult | TraineeResult | ReserveResult | ManagerResult;

export interface CalculationResults {
  formal: FormalResult[];
  trainee: TraineeResult[];
  reserve: ReserveResult[];
  manager: ManagerResult[];
  totalPerformance: number;
  totalConsumption: number;
  teamBonusPerPerson: number;
  teamBonusQualified: boolean;
}
