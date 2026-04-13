import { useState } from 'react';
import { Tabs, Table, Tag, Typography, Statistic, Row, Col, Card, Alert, Button, InputNumber } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import * as XLSX from 'xlsx';
import type { ColumnsType } from 'antd/es/table';
import type { TabsProps } from 'antd';
import type {
  CalculationResults,
  FormalResult,
  TraineeResult,
  ReserveResult,
  ManagerResult,
} from '../types';

const { Text } = Typography;

const fmt = (n: number) => n.toLocaleString();

// ─── Bonus override state ────────────────────────────────────────
type BonusKey = 'customerSatisfactionBonus' | 'otherBonus';
type BonusOverrides = Record<string, { customerSatisfactionBonus: number; otherBonus: number }>;

function getExtra(overrides: BonusOverrides, name: string) {
  return {
    customerSatisfactionBonus: overrides[name]?.customerSatisfactionBonus ?? 0,
    otherBonus: overrides[name]?.otherBonus ?? 0,
  };
}

// ─── Shared extra bonus columns ──────────────────────────────────
function extraBonusCols<T extends { name: string }>(
  overrides: BonusOverrides,
  setOverrides: React.Dispatch<React.SetStateAction<BonusOverrides>>
): ColumnsType<T> {
  const set = (name: string, field: BonusKey, value: number | null) => {
    setOverrides((prev) => ({
      ...prev,
      [name]: { ...getExtra(prev, name), [field]: value ?? 0 },
    }));
  };

  return [
    {
      title: '顧客好評獎金',
      key: 'customerSatisfactionBonus',
      width: 130,
      render: (_, r) => (
        <InputNumber
          min={0}
          step={100}
          value={getExtra(overrides, r.name).customerSatisfactionBonus}
          onChange={(v) => set(r.name, 'customerSatisfactionBonus', v)}
          style={{ width: 110 }}
          formatter={(v) => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
          parser={(v) => Number((v ?? '').replace(/,/g, ''))}
        />
      ),
    },
    {
      title: '其他加項獎金',
      key: 'otherBonus',
      width: 130,
      render: (_, r) => (
        <InputNumber
          min={0}
          step={100}
          value={getExtra(overrides, r.name).otherBonus}
          onChange={(v) => set(r.name, 'otherBonus', v)}
          style={{ width: 110 }}
          formatter={(v) => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
          parser={(v) => Number((v ?? '').replace(/,/g, ''))}
        />
      ),
    },
  ];
}

// ─── Formal ─────────────────────────────────────────────────────
function FormalTable({ data, overrides, setOverrides }: {
  data: FormalResult[];
  overrides: BonusOverrides;
  setOverrides: React.Dispatch<React.SetStateAction<BonusOverrides>>;
}) {
  const cols: ColumnsType<FormalResult> = [
    { title: '姓名', dataIndex: 'name', fixed: 'left', width: 90 },
    { title: '固定薪', dataIndex: 'fixedSalary', render: fmt },
    { title: '手技獎金', dataIndex: 'skillBonus', render: fmt },
    {
      title: '團獎',
      render: (_, r) => (
        <span>
          {fmt(r.teamBonus)}
          {r.teamBonusDisqualified && (
            <Text type="danger" style={{ fontSize: 11, display: 'block' }}>
              ✗ 指標未達標 ({r.failedMetrics.length}/3 未達)
            </Text>
          )}
          {!r.teamBonusDisqualified && r.teamBonusDeduction > 0 && (
            <Text type="warning" style={{ fontSize: 11, display: 'block' }}>
              業績{'<'}18萬扣 {fmt(r.teamBonusDeduction)}
            </Text>
          )}
        </span>
      ),
    },
    { title: '人次激勵', dataIndex: 'personCountBonus', render: fmt },
    { title: '充值目標獎', dataIndex: 'chargeTargetBonus', render: fmt },
    { title: '消耗獎勵', dataIndex: 'consumptionBonus', render: fmt },
    { title: '雙達標獎', dataIndex: 'dualTargetBonus', render: fmt },
    { title: '進階課程工獎', dataIndex: 'advancedCourseBonus', render: fmt },
    { title: '產品銷售工獎', dataIndex: 'productSalesBonus', render: fmt },
    { title: '新客成交率獎', dataIndex: 'newCustomerRateBonus', render: fmt },
    {
      title: '月薪小計',
      dataIndex: 'monthlyTotal',
      render: (v) => <Text strong>{fmt(v)}</Text>,
    },
    {
      title: '季獎小計',
      dataIndex: 'quarterlyTotal',
      render: (v) => <Text type="success">{fmt(v)}</Text>,
    },
    ...extraBonusCols<FormalResult>(overrides, setOverrides),
    {
      title: '合計',
      fixed: 'right',
      render: (_, r) => {
        const extra = getExtra(overrides, r.name);
        const total = r.grandTotal + extra.customerSatisfactionBonus + extra.otherBonus;
        return <Text strong type="danger">{fmt(total)}</Text>;
      },
    },
  ];
  return (
    <Table
      dataSource={data}
      columns={cols}
      rowKey="name"
      pagination={false}
      scroll={{ x: 'max-content' }}
      size="small"
    />
  );
}

// ─── Trainee ────────────────────────────────────────────────────
function TraineeTable({ data, overrides, setOverrides }: {
  data: TraineeResult[];
  overrides: BonusOverrides;
  setOverrides: React.Dispatch<React.SetStateAction<BonusOverrides>>;
}) {
  const cols: ColumnsType<TraineeResult> = [
    { title: '姓名', dataIndex: 'name', fixed: 'left', width: 90 },
    { title: '固定薪', dataIndex: 'fixedSalary', render: fmt },
    { title: '消耗×銷售獎金', dataIndex: 'consumptionSalesBonus', render: fmt },
    { title: '人次獎金', dataIndex: 'personCountBonus', render: fmt },
    { title: '進階課程工獎', dataIndex: 'advancedCourseBonus', render: fmt },
    { title: '產品銷售工獎', dataIndex: 'productSalesBonus', render: fmt },
    {
      title: '月薪小計',
      dataIndex: 'monthlyTotal',
      render: (v) => <Text strong>{fmt(v)}</Text>,
    },
    {
      title: '季獎小計',
      dataIndex: 'quarterlyTotal',
      render: (v) => <Text type="success">{fmt(v)}</Text>,
    },
    ...extraBonusCols<TraineeResult>(overrides, setOverrides),
    {
      title: '合計',
      fixed: 'right',
      render: (_, r) => {
        const extra = getExtra(overrides, r.name);
        const total = r.grandTotal + extra.customerSatisfactionBonus + extra.otherBonus;
        return <Text strong type="danger">{fmt(total)}</Text>;
      },
    },
  ];
  return (
    <Table
      dataSource={data}
      columns={cols}
      rowKey="name"
      pagination={false}
      scroll={{ x: 'max-content' }}
      size="small"
    />
  );
}

// ─── Reserve Manager ────────────────────────────────────────────
function ReserveTable({ data, overrides, setOverrides }: {
  data: ReserveResult[];
  overrides: BonusOverrides;
  setOverrides: React.Dispatch<React.SetStateAction<BonusOverrides>>;
}) {
  const cols: ColumnsType<ReserveResult> = [
    { title: '姓名', dataIndex: 'name', fixed: 'left', width: 90 },
    { title: '固定薪', dataIndex: 'fixedSalary', render: fmt },
    { title: '團獎(月)', dataIndex: 'teamBonus', render: fmt },
    { title: '達標獎金(月)', dataIndex: 'achievementBonus', render: fmt },
    { title: '訊息管理(月)', dataIndex: 'messageBonus', render: fmt },
    { title: '成交率獎(季)', dataIndex: 'conversionRateBonus', render: fmt },
    { title: '服務人次消耗獎(季)', dataIndex: 'serviceConsumptionBonus', render: fmt },
    { title: '店務管理獎(季)', dataIndex: 'storeManagementBonus', render: fmt },
    { title: '淨膚師目標達成獎(季)', dataIndex: 'therapistGoalBonus', render: fmt },
    {
      title: '月薪小計',
      dataIndex: 'monthlyTotal',
      render: (v) => <Text strong>{fmt(v)}</Text>,
    },
    {
      title: '季獎小計',
      dataIndex: 'quarterlyTotal',
      render: (v) => <Text type="success">{fmt(v)}</Text>,
    },
    ...extraBonusCols<ReserveResult>(overrides, setOverrides),
    {
      title: '合計',
      fixed: 'right',
      render: (_, r) => {
        const extra = getExtra(overrides, r.name);
        const total = r.grandTotal + extra.customerSatisfactionBonus + extra.otherBonus;
        return <Text strong type="danger">{fmt(total)}</Text>;
      },
    },
  ];
  return (
    <Table
      dataSource={data}
      columns={cols}
      rowKey="name"
      pagination={false}
      scroll={{ x: 'max-content' }}
      size="small"
    />
  );
}

// ─── Formal Manager ─────────────────────────────────────────────
function ManagerTable({ data, overrides, setOverrides }: {
  data: ManagerResult[];
  overrides: BonusOverrides;
  setOverrides: React.Dispatch<React.SetStateAction<BonusOverrides>>;
}) {
  const cols: ColumnsType<ManagerResult> = [
    { title: '姓名', dataIndex: 'name', fixed: 'left', width: 90 },
    { title: '固定薪', dataIndex: 'fixedSalary', render: fmt },
    { title: '團獎(月)', dataIndex: 'teamBonus', render: fmt },
    { title: '達標獎金(月)', dataIndex: 'achievementBonus', render: fmt },
    { title: '訊息管理(月)', dataIndex: 'messageBonus', render: fmt },
    { title: '管理津貼(月)', dataIndex: 'managementAllowance', render: fmt },
    { title: '成交率獎(季)', dataIndex: 'conversionRateBonus', render: fmt },
    { title: '服務人次消耗獎(季)', dataIndex: 'serviceConsumptionBonus', render: fmt },
    { title: '店務管理獎(季)', dataIndex: 'storeManagementBonus', render: fmt },
    {
      title: '月薪小計',
      dataIndex: 'monthlyTotal',
      render: (v) => <Text strong>{fmt(v)}</Text>,
    },
    {
      title: '季獎小計',
      dataIndex: 'quarterlyTotal',
      render: (v) => <Text type="success">{fmt(v)}</Text>,
    },
    ...extraBonusCols<ManagerResult>(overrides, setOverrides),
    {
      title: '合計',
      fixed: 'right',
      render: (_, r) => {
        const extra = getExtra(overrides, r.name);
        const total = r.grandTotal + extra.customerSatisfactionBonus + extra.otherBonus;
        return <Text strong type="danger">{fmt(total)}</Text>;
      },
    },
  ];
  return (
    <Table
      dataSource={data}
      columns={cols}
      rowKey="name"
      pagination={false}
      scroll={{ x: 'max-content' }}
      size="small"
    />
  );
}

// ─── Download helper ─────────────────────────────────────────────
function downloadExcel(sheetName: string, data: Record<string, unknown>[]) {
  const ws = XLSX.utils.json_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, sheetName);
  XLSX.writeFile(wb, `${sheetName}_薪資明細.xlsx`);
}

function enrichForExport<T extends { name: string; grandTotal: number }>(
  data: T[],
  overrides: BonusOverrides
): Record<string, unknown>[] {
  return data.map((r) => {
    const extra = getExtra(overrides, r.name);
    return {
      ...(r as unknown as Record<string, unknown>),
      顧客好評獎金: extra.customerSatisfactionBonus,
      其他加項獎金: extra.otherBonus,
      合計: r.grandTotal + extra.customerSatisfactionBonus + extra.otherBonus,
    };
  });
}

// ─── Summary ─────────────────────────────────────────────────────
function SummaryRow({ results, overrides }: { results: CalculationResults; overrides: BonusOverrides }) {
  const total = [
    ...results.formal,
    ...results.trainee,
    ...results.reserve,
    ...results.manager,
  ].reduce((sum, r) => {
    const extra = getExtra(overrides, r.name);
    return sum + r.grandTotal + extra.customerSatisfactionBonus + extra.otherBonus;
  }, 0);

  return (
    <Row gutter={16} style={{ marginBottom: 24 }}>
      <Col span={6}>
        <Card size="small">
          <Statistic title="總業績" value={results.totalPerformance} suffix="元" />
        </Card>
      </Col>
      <Col span={6}>
        <Card size="small">
          <Statistic title="總消耗" value={results.totalConsumption} suffix="元" />
        </Card>
      </Col>
      <Col span={6}>
        <Card size="small">
          <Statistic
            title="消耗比例"
            value={results.totalPerformance > 0 ? ((results.totalConsumption / results.totalPerformance) * 100).toFixed(1) : 0}
            suffix="%"
          />
        </Card>
      </Col>
      <Col span={6}>
        <Card size="small">
          <Statistic title="全店薪資總額" value={total} suffix="元" valueStyle={{ color: '#cf1322' }} />
        </Card>
      </Col>
    </Row>
  );
}

// ─── Main ────────────────────────────────────────────────────────
interface Props {
  results: CalculationResults;
}

export default function ResultTabs({ results }: Props) {
  const [bonusOverrides, setBonusOverrides] = useState<BonusOverrides>({});

  const teamLabel = results.teamBonusQualified
    ? <Tag color="green">團獎達標 ✓ 每人 {fmt(results.teamBonusPerPerson)} 元</Tag>
    : <Tag color="red">團獎未達標</Tag>;

  const items: TabsProps['items'] = [];

  if (results.formal.length > 0) {
    items.push({
      key: 'formal',
      label: `正式淨膚師 (${results.formal.length})`,
      children: (
        <>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => downloadExcel('正式淨膚師', enrichForExport(results.formal, bonusOverrides))}
            style={{ marginBottom: 12 }}
          >
            下載 Excel
          </Button>
          <FormalTable data={results.formal} overrides={bonusOverrides} setOverrides={setBonusOverrides} />
        </>
      ),
    });
  }
  if (results.trainee.length > 0) {
    items.push({
      key: 'trainee',
      label: `實習淨膚師 (${results.trainee.length})`,
      children: (
        <>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => downloadExcel('實習淨膚師', enrichForExport(results.trainee, bonusOverrides))}
            style={{ marginBottom: 12 }}
          >
            下載 Excel
          </Button>
          <TraineeTable data={results.trainee} overrides={bonusOverrides} setOverrides={setBonusOverrides} />
        </>
      ),
    });
  }
  if (results.reserve.length > 0) {
    items.push({
      key: 'reserve',
      label: `儲備店長 (${results.reserve.length})`,
      children: (
        <>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => downloadExcel('儲備店長', enrichForExport(results.reserve, bonusOverrides))}
            style={{ marginBottom: 12 }}
          >
            下載 Excel
          </Button>
          <ReserveTable data={results.reserve} overrides={bonusOverrides} setOverrides={setBonusOverrides} />
        </>
      ),
    });
  }
  if (results.manager.length > 0) {
    items.push({
      key: 'manager',
      label: `正式店長 (${results.manager.length})`,
      children: (
        <>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => downloadExcel('正式店長', enrichForExport(results.manager, bonusOverrides))}
            style={{ marginBottom: 12 }}
          >
            下載 Excel
          </Button>
          <ManagerTable data={results.manager} overrides={bonusOverrides} setOverrides={setBonusOverrides} />
        </>
      ),
    });
  }

  return (
    <div>
      <SummaryRow results={results} overrides={bonusOverrides} />
      <div style={{ marginBottom: 12 }}>{teamLabel}</div>
      {items.length === 0 ? (
        <Alert message="尚無計算結果" type="info" />
      ) : (
        <Tabs items={items} />
      )}
    </div>
  );
}
