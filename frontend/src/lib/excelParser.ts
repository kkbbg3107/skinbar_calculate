import * as XLSX from 'xlsx';
import type { ExcelData, RawEmployee } from '../types';

function toNum(val: unknown): number {
  if (val === null || val === undefined) return 0;
  const n = Number(val);
  return isNaN(n) ? 0 : n;
}

/**
 * Parse an Excel file (ArrayBuffer) and return structured data.
 * Reads the 「月報表彙整」 sheet for employee rows, and date sheets for
 * total performance, consumption, and mask sales.
 */
export async function parseExcel(file: File): Promise<ExcelData> {
  const buffer = await file.arrayBuffer();
  const workbook = XLSX.read(buffer, { type: 'array' });

  const summarySheetName = '月報表彙整';
  if (!workbook.SheetNames.includes(summarySheetName)) {
    throw new Error('找不到「月報表彙整」工作表，請確認 Excel 檔案格式正確');
  }

  const summarySheet = workbook.Sheets[summarySheetName];
  // Convert to 2D array (no header, raw values)
  const rows: unknown[][] = XLSX.utils.sheet_to_json(summarySheet, {
    header: 1,
    defval: null,
    raw: true,
  });

  // Find date sheets (exclude 月報表彙整, keep numeric-named sheets)
  const dateSheets = workbook.SheetNames.filter(
    (name) => name !== summarySheetName && /^\d/.test(name)
  ).sort();

  // ─── Total performance & consumption from date sheets ───────
  let totalPerformance = 0;
  let totalConsumption = 0;

  for (const sheetName of dateSheets) {
    const sheet = workbook.Sheets[sheetName];
    const sheetRows: unknown[][] = XLSX.utils.sheet_to_json(sheet, {
      header: 1,
      defval: null,
      raw: true,
    });
    // E3 = row index 2, col index 4
    if (sheetRows[2] && sheetRows[2][4] != null) {
      totalPerformance += toNum(sheetRows[2][4]);
    }
    // E5 = row index 4, col index 4
    if (sheetRows[4] && sheetRows[4][4] != null) {
      totalConsumption += toNum(sheetRows[4][4]);
    }
  }

  // ─── Product sales (任何產品) from date sheets ───────────────
  const maskSales: Record<string, number> = {};

  for (const sheetName of dateSheets) {
    const sheet = workbook.Sheets[sheetName];
    const sheetRows: unknown[][] = XLSX.utils.sheet_to_json(sheet, {
      header: 1,
      defval: null,
      raw: true,
    });

    // Start from row 21 (index 20), check F/G/H columns (5/6/7)
    for (let rowIdx = 20; rowIdx < sheetRows.length; rowIdx++) {
      const row = sheetRows[rowIdx];
      if (!row) continue;
      for (const colIdx of [5, 6, 7]) {
        const cellVal = row[colIdx];
        if (cellVal != null && String(cellVal).trim() !== '') {
          // N column = index 13
          const therapistId = row[13];
          if (therapistId != null) {
            const key = String(Math.round(Number(therapistId)));
            maskSales[key] = (maskSales[key] ?? 0) + 1;
          }
          break;
        }
      }
    }
  }

  // ─── Monthly target from E23 (月報表彙整 row index 22, col index 4) ──
  const monthlyTarget = rows[22] ? toNum(rows[22][4]) : 0;

  // ─── Employee rows from 月報表彙整 ───────────────────────────
  const employees: RawEmployee[] = [];
  const START_ROW = 14; // 1-based, so index 13

  let consecutiveZeros = 0;
  const maxRow = Math.min(rows.length, START_ROW + 20);

  for (let rowIdx = START_ROW - 1; rowIdx < maxRow; rowIdx++) {
    const row = rows[rowIdx];
    if (!row) continue;

    const name = row[0]; // A
    const bVal = row[1]; // B (personal performance)

    // Skip if B is text (header)
    if (bVal != null && isNaN(Number(bVal))) continue;

    const bNum = toNum(bVal);

    if (bNum === 0) {
      consecutiveZeros++;
      if (consecutiveZeros >= 2) break;
      continue;
    }
    consecutiveZeros = 0;

    if (name == null || String(name).trim() === '') continue;
    const nameStr = String(name).trim();
    if (/^\d+$/.test(nameStr)) continue; // skip pure numeric names

    employees.push({
      row: rowIdx + 1, // 1-based
      name: nameStr,
      personalPerformance: bNum,
      personalConsumption: toNum(row[2]),  // C
      personCount: toNum(row[3]),          // D
      newCustomerRate: toNum(row[8]),      // I：新客成交率
      vipUpgradeRate: toNum(row[17]),      // R：VIP成交率
      appointmentRate: toNum(row[23]),     // X：預約率
      advancedCourseBonus: toNum(row[18]), // S：進階工獎累計
      skillBonusTotal: toNum(row[19]),     // T：手技工獎累計
      productSalesBonus: toNum(row[20]),   // U：產品銷售工獎
    });
  }

  if (employees.length === 0) {
    throw new Error('無法找到員工數據，請確認月報表彙整工作表格式正確（員工資料應從第14行開始）');
  }

  return { employees, totalPerformance, totalConsumption, monthlyTarget, maskSales };
}
