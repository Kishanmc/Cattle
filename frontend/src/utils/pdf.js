export function downloadPdf(prediction) {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF();
    let y = 10;
  
    pdf.setFontSize(16);
    pdf.text("Cattle Vision Report", 10, y);
    y += 10;
  
    pdf.setFontSize(12);
    pdf.text(`Class: ${prediction.predicted_class}`, 10, y); y += 7;
    pdf.text(`Confidence: ${(prediction.confidence * 100).toFixed(2)}%`, 10, y);
  
    pdf.save("prediction_report.pdf");
  }
  