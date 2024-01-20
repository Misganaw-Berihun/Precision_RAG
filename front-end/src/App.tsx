import React, { useState } from "react";
import axios from "axios";
import {
  Button,
  TextField,
  Typography,
  Paper,
  Container,
  Grid,
} from "@material-ui/core";

const App = () => {
  const [description, setDescription] = useState("");
  const [scenarios, setScenarios] = useState([]);
  const [expectedOutputs, setExpectedOutputs] = useState([]);
  const [generatedPrompts, setGeneratedPrompts] = useState([]);
  const [evaluationData, setEvaluationData] = useState([]);

  const generatePrompts = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/generate_prompts",
        {
          description,
          scenarios,
          expectedOutputs,
        }
      );
      setGeneratedPrompts(response.data.prompts);
    } catch (error) {
      console.error("Error generating prompts:", error);
    }
  };

  const generateEvaluationData = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/generate_evaluation_data",
        {
          description,
          scenarios,
          expectedOutputs,
        }
      );
      setEvaluationData(response.data.evaluation_data);
    } catch (error) {
      console.error("Error generating evaluation data:", error);
    }
  };

  return (
    <Container component="main" maxWidth="md">
      <Paper elevation={3} style={{ padding: 20, marginTop: 50 }}>
        <Typography variant="h4" align="center" gutterBottom>
          Prompt Generation System
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              fullWidth
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              variant="outlined"
              fullWidth
              label="Scenario"
              value={scenarios[0] || ""}
              onChange={(e) => setScenarios([e.target.value])}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              variant="outlined"
              fullWidth
              label="Expected Output"
              value={expectedOutputs[0] || ""}
              onChange={(e) => setExpectedOutputs([e.target.value])}
            />
          </Grid>
        </Grid>

        <Button
          variant="contained"
          color="primary"
          onClick={generatePrompts}
          style={{ marginTop: 20 }}
        >
          Generate Prompts
        </Button>

        <Button
          variant="contained"
          color="secondary"
          onClick={generateEvaluationData}
          style={{ marginTop: 20, marginLeft: 10 }}
        >
          Generate Evaluation Data
        </Button>

        <Typography variant="h5" align="center" style={{ marginTop: 30 }}>
          Generated Prompts:
        </Typography>
        {generatedPrompts.map((prompt, index) => (
          <Typography key={index} variant="body1">
            {prompt}
          </Typography>
        ))}

        <Typography variant="h5" align="center" style={{ marginTop: 30 }}>
          Evaluation Data:
        </Typography>
        {evaluationData.map((data, index) => (
          <Typography key={index} variant="body1">
            Prompt: {data.prompt}, Score: {data.evaluation_score}
          </Typography>
        ))}
      </Paper>
    </Container>
  );
};

export default App;
