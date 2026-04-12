import { useState } from 'react';
import { Layout, Steps, Button, Typography, Divider, Alert, ConfigProvider, theme } from 'antd';
import zhTW from 'antd/locale/zh_TW';
import FileUpload from './components/FileUpload';
import RoleAssignment from './components/RoleAssignment';
import ResultTabs from './components/ResultTabs';
import type { ExcelData, EmployeeWithRole, CalculationResults } from './types';
import { calculateAll } from './lib/salary/calculator';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

const STEP_UPLOAD = 0;
const STEP_ASSIGN = 1;
const STEP_RESULT = 2;

function App() {
  const [step, setStep] = useState(STEP_UPLOAD);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [excelData, setExcelData] = useState<ExcelData | null>(null);
  const [assignments, setAssignments] = useState<EmployeeWithRole[]>([]);
  const [results, setResults] = useState<CalculationResults | null>(null);

  const handleParsed = (data: ExcelData) => {
    setExcelData(data);
    const defaultAssignments: EmployeeWithRole[] = data.employees.map((e, idx) => ({
      ...e,
      role: '正式淨膚師',
      therapistId: idx + 1,
    }));
    setAssignments(defaultAssignments);
    setStep(STEP_ASSIGN);
  };

  const handleCalculate = () => {
    if (!excelData) return;
    try {
      const r = calculateAll(assignments, excelData);
      setResults(r);
      setStep(STEP_RESULT);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '計算失敗');
    }
  };

  const handleReset = () => {
    setStep(STEP_UPLOAD);
    setExcelData(null);
    setAssignments([]);
    setResults(null);
    setError(null);
  };

  const formalCount = assignments.filter((e) => e.role === '正式淨膚師').length;
  const canCalculate = formalCount >= 2 && formalCount <= 6;

  return (
    <ConfigProvider locale={zhTW} theme={{ algorithm: theme.defaultAlgorithm }}>
      <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
        <Header style={{ background: '#1677ff', padding: '0 24px', display: 'flex', alignItems: 'center' }}>
          <Title level={4} style={{ color: '#fff', margin: 0 }}>
            💰 淨膚寶薪資計算系統
          </Title>
        </Header>
        <Content style={{ padding: '24px', maxWidth: 1400, margin: '0 auto', width: '100%' }}>
          <Steps
            current={step}
            style={{ marginBottom: 32 }}
            items={[
              { title: '上傳 Excel' },
              { title: '指派職務' },
              { title: '薪資結果' },
            ]}
          />

          {error && (
            <Alert
              type="error"
              message={error}
              closable
              onClose={() => setError(null)}
              style={{ marginBottom: 16 }}
            />
          )}

          {step === STEP_UPLOAD && (
            <div>
              <Title level={4}>步驟 1：上傳月報表 Excel</Title>
              <FileUpload
                onParsed={handleParsed}
                loading={loading}
                setLoading={setLoading}
                error={null}
                setError={setError}
              />
            </div>
          )}

          {step === STEP_ASSIGN && excelData && (
            <div>
              <Title level={4}>步驟 2：指派職務</Title>
              <Text type="secondary">
                已讀取 {excelData.employees.length} 位員工。
                總業績：{excelData.totalPerformance.toLocaleString()} 元 ／
                總消耗：{excelData.totalConsumption.toLocaleString()} 元
              </Text>
              <Divider />
              <RoleAssignment
                assignments={assignments}
                onChange={setAssignments}
              />
              <Divider />
              {!canCalculate && (
                <Alert
                  type="warning"
                  message={`正式淨膚師人數須為 2-6 位（目前 ${formalCount} 位）才能計算團獎`}
                  style={{ marginBottom: 16 }}
                />
              )}
              <Button
                type="primary"
                size="large"
                onClick={handleCalculate}
                disabled={assignments.length === 0}
              >
                開始計算薪資
              </Button>
              <Button style={{ marginLeft: 12 }} onClick={handleReset}>重新上傳</Button>
            </div>
          )}

          {step === STEP_RESULT && results && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
                <Title level={4} style={{ margin: 0 }}>步驟 3：薪資計算結果</Title>
                <Button onClick={handleReset}>重新計算</Button>
              </div>
              <ResultTabs results={results} />
            </div>
          )}
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default App;
