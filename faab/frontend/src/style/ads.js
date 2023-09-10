import { createTheme } from "@material-ui/core/styles";

const myTheme = createTheme({

  mainheader: {
    paddingTop: '100px;,'
  },
  overrides: {
    MuiAppBar: {
      colorPrimary: {
        backgroundColor: "#4F6D7A",
        color: "#EAEAEA"
      },
    },
    MuiTableCell: {
      root: {
        textAlign: "center",
        color: "#4F6D7A"
      },
      
      
    },  

    MuiTypography: {
      a: {
        color: "#EAEAEA",
      },
      body2: {
        paddingTop: "20px",
        marginTop: "10px",
        backgroundColor: "#EAEAEA",
        color: "#EAEAEA"
      },
      h4: {
        paddingTop: "20px",
        backgroundColor: "#EAEAEA",
        color: "#EAEAEA"
      },
      h5: {
        marginTop: "20px",
        backgroundColor: "#EAEAEA",
        color: "#4F6D7A"
      },
      h7: {
        paddingTop: "10px",
        paddingBottom: "15px",
        backgroundColor: "#EAEAEA",
        color: "#4F6D7A"
      },
      gutterBottom: {
        paddingTop: "40px",
        backgroundColor: "#EAEAEA",
        color: "#4F6D7A"
      },
    },  
    MuiBox: {
      img: {
        maxWidth: '100%',
        height: 'auto',
        display: 'block', 
      },
      root: {
        // maxWidth: '100%',
        // height: 'auto',
        // display: 'block', 
        backgroundColor: "#EAEAEA",
        color: "#4F6D7A"
      },
    },  
    // MuiCardMedia: {
    //   root: {
    //     backgroundColor: "#C0D6DF",
    //     paddingBottom: "50px"
    //   },
    // },
    MuiCardContent: {
      root: {
        borderStyle: "solid",
        borderColor: "#DD6E42",
        backgroundColor: "#C0D6DF",
        color: "#4F6D7A"
      },
    },
    MuiContainer: {
      root: {
        backgroundColor: "#EAEAEA",
        color: "#4F6D7A"
      },
    },
    MuiButton: {
        root: {
          borderStyle: "solid",
          borderColor: "#DD6E42",
          margin: "20px",
        },
        contained: {
          borderStyle: "solid",
          borderColor: "#DD6E42",
          backgroundColor: "#4F6D7A",
          color: "#EAEAEA"
        },
        containedPrimary: {
          borderStyle: "solid",
          borderColor: "#DD6E42",
          backgroundColor: "#4F6D7A",
          color: "#EAEAEA"
        },
      },
  },
});

export default createTheme(myTheme);