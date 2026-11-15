// E2E-сценарій викладача: сторінка відкривається, API справне, опитування створюється з шаблону.
describe('SurveyLab: сторінка викладача', () => {
  it('показує стан API', () => {
    cy.visit('/');
    cy.contains('SurveyLab');
    cy.get('#status').should('contain', 'Стан API: ok').and('contain', 'postgres');
  });

  it('створює опитування з шаблону й показує його у списку', () => {
    const title = 'E2E: Основи DevOps, КН-41 ' + Date.now();
    cy.visit('/');
    cy.get('#title').type(title);
    cy.contains('button', 'Створити опитування').click();
    cy.get('#surveys li').should('contain', title).and('contain', 'Питань: 3');
  });

  it('API повертає створені опитування', () => {
    cy.request('/api/surveys').its('body').should('have.length.greaterThan', 0);
  });
});
