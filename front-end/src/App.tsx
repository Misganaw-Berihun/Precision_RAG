import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Button,
  TextField,
  Typography,
  Paper,
  Container,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@material-ui/core";

const App = () => {
  const [objective, setObjective] = useState([]);
  const [expectedOutputs, setExpectedOutputs] = useState([]);
  const [generatedPrompts, setGeneratedPrompts] = useState([]);
  const [file, setFile] = useState(null);

  const generatePrompts = async () => {
    try {
      const formData = new FormData();
      formData.append("objectives", JSON.stringify(objective));
      formData.append("expectedOutputs", JSON.stringify(expectedOutputs));
      formData.append("file", file);

      const response = await axios.post(
        "http://localhost:5000/api/generate_prompts",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Assuming the response contains an array of objects with prompt and score
      setGeneratedPrompts(response.data);
    } catch (error) {
      console.error("Error generating prompts:", error);
    }
  };

  const fetchPrompts = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/prompts");
      setGeneratedPrompts(response.data.prompts);
    } catch (error) {
      console.error("Error fetching prompts:", error);
    }
  };

  // Use useEffect to fetch prompts when the component mounts
  useEffect(() => {
    fetchPrompts();
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  return (
    <div>
      <Container component="main" maxWidth="md">
        <Paper elevation={3} style={{ padding: 20, marginTop: 50 }}>
          <Typography variant="h4" align="center" gutterBottom>
            Prompt Generation System
          </Typography>

          <Grid container spacing={2}>
            <Grid item xs={6}>
              <TextField
                variant="outlined"
                fullWidth
                label="Objective"
                value={objective[0] || ""}
                onChange={(e) => setObjective([e.target.value])}
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
            <Grid item xs={6}>
              <input type="file" onChange={handleFileChange} />
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
            onClick={fetchPrompts}
            style={{ marginLeft: 10, marginTop: 20 }}
          >
            Fetch Prompts
          </Button>

          {generatedPrompts.length > 0 && (
            <>
              <Typography variant="h5" align="center" style={{ marginTop: 30 }}>
                Generated Prompts:
              </Typography>
              <TableContainer component={Paper} style={{ marginTop: 10 }}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell style={{ width: "85%" }}>Prompt</TableCell>
                      <TableCell style={{ width: "15%" }}>Score (%)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {generatedPrompts.map((prompt, index) => (
                      <TableRow key={index}>
                        <TableCell>{prompt}</TableCell>
                        <TableCell>{70}%</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </>
          )}
        </Paper>
      </Container>
    </div>
  );
};

export default App;
